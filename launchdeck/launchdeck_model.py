import json
import uuid
import os
from datetime import datetime
from database import get_db_connection

def is_admin(user_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        return row and row['role'] == 'admin'
    finally:
        conn.close()

def create_student_mentorship_request(student_id, alumni_id, message):
    conn = get_db_connection()
    try:
        student = conn.execute('SELECT role FROM users WHERE id = ?', (student_id,)).fetchone()
        if not student or student['role'] != 'student':
            return False, "Only students can request mentorship", 403
            
        alumni = conn.execute('SELECT role FROM users WHERE id = ?', (alumni_id,)).fetchone()
        if not alumni or alumni['role'] not in ('alumni', 'mentor', 'founder', 'investor'):
            return False, "Invalid alumni ID", 400
            
        existing = conn.execute('SELECT id FROM mentorship_requests WHERE student_id = ? AND alumni_id = ?', (student_id, alumni_id)).fetchone()
        if existing:
            return False, "You have already sent a mentorship request to this alumni", 400
            
        conn.execute('''
            INSERT INTO mentorship_requests (student_id, alumni_id, message, status, created_at)
            VALUES (?, ?, ?, 'pending', datetime('now'))
        ''', (student_id, alumni_id, message))
        conn.commit()
        return True, "Mentorship request sent successfully", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_student_mentorship_requests(user_id):
    conn = get_db_connection()
    try:
        user_role = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        if not user_role:
            return None, "User not found", 404
            
        if user_role['role'] == 'student':
            rows = conn.execute('''
                SELECT mr.id, mr.message, mr.status, mr.created_at,
                       u.name as other_user_name, u.email as other_user_email
                FROM mentorship_requests mr
                LEFT JOIN users u ON mr.alumni_id = u.id
                WHERE mr.student_id = ?
                ORDER BY mr.created_at DESC
            ''', (user_id,)).fetchall()
        else:
            rows = conn.execute('''
                SELECT mr.id, mr.message, mr.status, mr.created_at,
                       u.name as other_user_name, u.email as other_user_email
                FROM mentorship_requests mr
                LEFT JOIN users u ON mr.student_id = u.id
                WHERE mr.alumni_id = ?
                ORDER BY mr.created_at DESC
            ''', (user_id,)).fetchall()
            
        return [dict(r) for r in rows], None, 200
    finally:
        conn.close()

def handle_student_mentorship_request(user_id, request_id, action):
    conn = get_db_connection()
    try:
        req = conn.execute('''
            SELECT mr.id, mr.alumni_id, u.role
            FROM mentorship_requests mr
            JOIN users u ON mr.alumni_id = u.id
            WHERE mr.id = ?
        ''', (request_id,)).fetchone()
        
        if not req: return False, "Mentorship request not found", 404
        if req['alumni_id'] != user_id: return False, "You can only handle your own mentorship requests", 403
        if req['role'] not in ('alumni', 'mentor', 'founder', 'investor'): return False, "Only alumni can handle mentorship requests", 403
        
        new_status = 'accepted' if action == 'accept' else 'declined'
        conn.execute('UPDATE mentorship_requests SET status = ? WHERE id = ?', (new_status, request_id))
        conn.commit()
        return True, f"Mentorship request {action}ed successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_pitches(status='published', category=None, search=None):
    conn = get_db_connection()
    try:
        query = '''
            SELECT p.id, p.title, p.tagline, p.logo, p.category, p.status, p.created_at,
                   u.name as founder_name, u.avatar as founder_avatar, p.pitch_overview, p.pitch_deck_images
            FROM pitches p
            JOIN users u ON p.founder_id = u.id
            WHERE p.status = ?
        '''
        params = [status]
        if category:
            query += ' AND p.category = ?'
            params.append(category)
        if search:
            query += ' AND (p.title LIKE ? OR p.tagline LIKE ? OR p.pitch_overview LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%', f'%{search}%'])
        
        query += ' ORDER BY p.created_at DESC'
        rows = conn.execute(query, params).fetchall()
        
        pitches = []
        for r in rows:
            p = dict(r)
            try: p['pitch_deck_images'] = json.loads(p['pitch_deck_images']) if p['pitch_deck_images'] else []
            except: p['pitch_deck_images'] = []
            pitches.append(p)
        return pitches
    finally:
        conn.close()

def get_pitch_detail(pitch_id):
    conn = get_db_connection()
    try:
        row = conn.execute('''
            SELECT p.*, u.name as founder_name, u.avatar as founder_avatar, u.email as founder_email
            FROM pitches p
            JOIN users u ON p.founder_id = u.id
            WHERE p.id = ?
        ''', (pitch_id,)).fetchone()
        
        if not row: return None
        
        p = dict(row)
        for field in ['highlights', 'team_members', 'pitch_deck_images', 'social_links']:
            try: p[field] = json.loads(p[field]) if p[field] else ([] if field != 'social_links' else {})
            except: p[field] = [] if field != 'social_links' else {}
            
        interest_count = conn.execute('SELECT COUNT(*) as c FROM pitch_interests WHERE pitch_id = ?', (pitch_id,)).fetchone()['c']
        p['interest_count'] = interest_count
        return p
    finally:
        conn.close()

def create_pitch(founder_id, data):
    conn = get_db_connection()
    try:
        # Check if founder
        user = conn.execute('SELECT role FROM users WHERE id = ?', (founder_id,)).fetchone()
        if not user or user['role'] != 'founder':
            return None, "Only founders can create pitches", 403
            
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pitches (founder_id, title, tagline, logo, pitch_overview, highlights,
                                 team_members, pitch_deck_images, category, website, social_links, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            founder_id, data.get('title', ''), data.get('tagline', ''), data.get('logo', ''),
            data.get('pitch_overview', ''), json.dumps(data.get('highlights', [])),
            json.dumps(data.get('team_members', [])), json.dumps(data.get('pitch_deck_images', [])),
            data.get('category', ''), data.get('website', ''), json.dumps(data.get('social_links', {})),
            data.get('status', 'draft')
        ))
        conn.commit()
        return cursor.lastrowid, "Success", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_pitch(user_id, pitch_id, data):
    conn = get_db_connection()
    try:
        pitch = conn.execute('SELECT founder_id FROM pitches WHERE id = ?', (pitch_id,)).fetchone()
        if not pitch: return False, "Pitch not found", 404
        if pitch['founder_id'] != user_id and not is_admin(user_id): return False, "Unauthorized", 403
        
        conn.execute('''
            UPDATE pitches SET title=?, tagline=?, logo=?, pitch_overview=?, highlights=?,
                   team_members=?, pitch_deck_images=?, category=?, website=?, social_links=?,
                   status=?, updated_at=CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            data.get('title', ''), data.get('tagline', ''), data.get('logo', ''), data.get('pitch_overview', ''),
            json.dumps(data.get('highlights', [])), json.dumps(data.get('team_members', [])),
            json.dumps(data.get('pitch_deck_images', [])), data.get('category', ''),
            data.get('website', ''), json.dumps(data.get('social_links', {})), data.get('status', 'draft'),
            pitch_id
        ))
        conn.commit()
        return True, "Success", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_pitch(user_id, pitch_id):
    conn = get_db_connection()
    try:
        pitch = conn.execute('SELECT founder_id FROM pitches WHERE id = ?', (pitch_id,)).fetchone()
        if not pitch: return False, "Pitch not found", 404
        if pitch['founder_id'] != user_id and not is_admin(user_id): return False, "Unauthorized", 403
        
        conn.execute('DELETE FROM pitch_interests WHERE pitch_id = ?', (pitch_id,))
        conn.execute('DELETE FROM launchdeck_mentorship_requests WHERE pitch_id = ?', (pitch_id,))
        conn.execute('DELETE FROM pitches WHERE id = ?', (pitch_id,))
        conn.commit()
        return True, "Deleted", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_my_pitches(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute('''
            SELECT p.id, p.title, p.tagline, p.logo, p.category, p.status, p.created_at,
                   (SELECT COUNT(*) FROM pitch_interests WHERE pitch_id = p.id) as interest_count,
                   (SELECT COUNT(*) FROM launchdeck_mentorship_requests WHERE pitch_id = p.id) as mentorship_count
            FROM pitches p
            WHERE p.founder_id = ?
            ORDER BY p.created_at DESC
        ''', (user_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def submit_interest(user_id, pitch_id, message):
    conn = get_db_connection()
    try:
        pitch = conn.execute('SELECT title FROM pitches WHERE id = ? AND status = ?', (pitch_id, 'published')).fetchone()
        if not pitch: return False, "Pitch not found", 404
        
        existing = conn.execute('SELECT id FROM pitch_interests WHERE pitch_id = ? AND investor_id = ?', (pitch_id, user_id)).fetchone()
        if existing: return False, "Already expressed interest", 400
        
        conn.execute('''
            INSERT INTO pitch_interests (pitch_id, investor_id, message, status)
            VALUES (?, ?, ?, 'pending')
        ''', (pitch_id, user_id, message))
        
        investor_name = conn.execute('SELECT name FROM users WHERE id = ?', (user_id,)).fetchone()['name']
        conn.execute('''
            INSERT INTO admin_notifications (type, reference_id, message)
            VALUES (?, ?, ?)
        ''', ('interest_request', pitch_id, f'{investor_name} expressed interest in "{pitch["title"]}"'))
        
        conn.commit()
        return True, "Interest submitted", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def check_interest(user_id, pitch_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT status FROM pitch_interests WHERE pitch_id = ? AND investor_id = ?', (pitch_id, user_id)).fetchone()
        if row: return {'has_interest': True, 'status': row['status']}
        return {'has_interest': False}
    finally:
        conn.close()

def launchdeck_request_mentorship(user_id, pitch_id, message):
    conn = get_db_connection()
    try:
        pitch = conn.execute('SELECT title FROM pitches WHERE id = ? AND founder_id = ?', (pitch_id, user_id)).fetchone()
        if not pitch: return False, "Pitch not found or not yours", 404
        
        existing = conn.execute('SELECT id FROM launchdeck_mentorship_requests WHERE pitch_id = ? AND founder_id = ?', (pitch_id, user_id)).fetchone()
        if existing: return False, "Mentorship already requested for this pitch", 400
        
        conn.execute('''
            INSERT INTO launchdeck_mentorship_requests (pitch_id, founder_id, message, status)
            VALUES (?, ?, ?, 'pending')
        ''', (pitch_id, user_id, message))
        
        founder_name = conn.execute('SELECT name FROM users WHERE id = ?', (user_id,)).fetchone()['name']
        conn.execute('''
            INSERT INTO admin_notifications (type, reference_id, message)
            VALUES (?, ?, ?)
        ''', ('mentorship_request', pitch_id, f'{founder_name} requested mentorship for "{pitch["title"]}"'))
        
        conn.commit()
        return True, "Request submitted", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_launchdeck_mentorship_requests(user_id):
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        if user and user['role'] in ('mentor', 'alumni'):
            rows = conn.execute('''
                SELECT mr.*, p.title as pitch_title, p.tagline as pitch_tagline, p.logo as pitch_logo, p.category as pitch_category,
                       u.name as founder_name, u.avatar as founder_avatar
                FROM launchdeck_mentorship_requests mr
                JOIN pitches p ON mr.pitch_id = p.id
                JOIN users u ON mr.founder_id = u.id
                WHERE mr.mentor_id = ? OR (mr.mentor_id IS NULL AND mr.status = 'pending')
                ORDER BY mr.created_at DESC
            ''', (user_id,)).fetchall()
        elif user and user['role'] in ('founder', 'investor'):
            # Founders/investors see their own mentorship requests
            rows = conn.execute('''
                SELECT mr.*, p.title as pitch_title, p.tagline as pitch_tagline, p.logo as pitch_logo, p.category as pitch_category,
                       u.name as founder_name, u.avatar as founder_avatar
                FROM launchdeck_mentorship_requests mr
                JOIN pitches p ON mr.pitch_id = p.id
                JOIN users u ON mr.founder_id = u.id
                WHERE mr.founder_id = ?
                ORDER BY mr.created_at DESC
            ''', (user_id,)).fetchall()
        elif user and user['role'] == 'admin':
            rows = conn.execute('''
                SELECT mr.*, p.title as pitch_title, p.tagline as pitch_tagline, p.logo as pitch_logo, p.category as pitch_category,
                       u.name as founder_name, u.avatar as founder_avatar
                FROM launchdeck_mentorship_requests mr
                JOIN pitches p ON mr.pitch_id = p.id
                JOIN users u ON mr.founder_id = u.id
                ORDER BY mr.created_at DESC
            ''').fetchall()
        else:
            return None, "Access denied", 403
            
        requests = []
        for r in rows:
            req = dict(r)
            if req['mentor_id']:
                mentor = conn.execute('SELECT name FROM users WHERE id = ?', (req['mentor_id'],)).fetchone()
                req['mentor_name'] = mentor['name'] if mentor else None
            else:
                req['mentor_name'] = None
            requests.append(req)
        return requests, None, 200
    finally:
        conn.close()

def update_launchdeck_mentorship_request(user_id, request_id, status):
    conn = get_db_connection()
    try:
        req = conn.execute('SELECT mentor_id FROM launchdeck_mentorship_requests WHERE id = ?', (request_id,)).fetchone()
        if not req: return False, "Request not found", 404
        if req['mentor_id'] != user_id and not is_admin(user_id): return False, "Unauthorized", 403
        
        conn.execute('UPDATE launchdeck_mentorship_requests SET status = ? WHERE id = ?', (status, request_id))
        conn.commit()
        return True, "Updated successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_admin_notifications(user_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin required", 403
        rows = conn.execute('''
            SELECT id, type, reference_id, message, is_read, created_at
            FROM admin_notifications ORDER BY created_at DESC LIMIT 50
        ''').fetchall()
        return [dict(r) for r in rows], None, 200
    finally:
        conn.close()

def mark_admin_notification_read(user_id, notif_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return False, "Admin required", 403
        conn.execute('UPDATE admin_notifications SET is_read = 1 WHERE id = ?', (notif_id,))
        conn.commit()
        return True, "Marked read", 200
    finally:
        conn.close()

def assign_mentor(user_id, request_id, mentor_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return False, "Admin required", 403
        req = conn.execute('SELECT id FROM launchdeck_mentorship_requests WHERE id = ?', (request_id,)).fetchone()
        if not req: return False, "Request not found", 404
        mentor = conn.execute('SELECT role FROM users WHERE id = ?', (mentor_id,)).fetchone()
        if not mentor or mentor['role'] != 'mentor': return False, "Invalid mentor", 400
        
        conn.execute('UPDATE launchdeck_mentorship_requests SET mentor_id = ? WHERE id = ?', (mentor_id, request_id))
        conn.commit()
        return True, "Assigned successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_launchdeck_mentors(user_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin required", 403
        rows = conn.execute('SELECT id, name, email FROM users WHERE role = ?', ('mentor',)).fetchall()
        return [dict(r) for r in rows], None, 200
    finally:
        conn.close()

def get_all_interests(user_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin required", 403
        rows = conn.execute('''
            SELECT pi.id, pi.pitch_id, pi.investor_id, pi.message, pi.status, pi.created_at,
                   u.name as investor_name, u.email as investor_email, p.title as pitch_title
            FROM pitch_interests pi
            JOIN users u ON pi.investor_id = u.id
            JOIN pitches p ON pi.pitch_id = p.id
            ORDER BY pi.created_at DESC
        ''').fetchall()
        return [dict(r) for r in rows], None, 200
    finally:
        conn.close()

def update_interest_status(user_id, interest_id, status):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return False, "Admin required", 403
        conn.execute('UPDATE pitch_interests SET status = ? WHERE id = ?', (status, interest_id))
        conn.commit()
        return True, "Updated successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
