import sqlite3
import json
from database import get_db_connection

def get_user_data(user_id):
    conn = get_db_connection()
    try:
        user_data = conn.execute('''
            SELECT id, name, email, role, graduation_year, department, hall, branch, bio,
                   current_company, current_position, location, work_preference,
                   phone, website, linkedin, github, avatar, program, joining_year,
                   institute, specialization, past_projects, cv_pdf, is_available,
                   roll_number, id_card_image
            FROM users WHERE id = ?
        ''', (user_id,)).fetchone()
        
        if not user_data:
            return None
            
        skills_data = conn.execute('SELECT skill_name, skill_type, proficiency_level FROM user_skills WHERE user_id = ?', (user_id,)).fetchall()
        achievements_data = conn.execute('SELECT title, description, achievement_type, date_earned, issuer FROM user_achievements WHERE user_id = ?', (user_id,)).fetchall()
        languages_data = conn.execute('SELECT language_name, proficiency_level FROM user_languages WHERE user_id = ?', (user_id,)).fetchall()
        
        user_dict = dict(user_data)
        user_dict['past_projects'] = json.loads(user_dict['past_projects']) if user_dict['past_projects'] else []
        user_dict['is_available'] = bool(user_dict['is_available']) if user_dict['is_available'] is not None else True
        user_dict['skills'] = [{'name': s['skill_name'], 'type': s['skill_type'], 'proficiency': s['proficiency_level']} for s in skills_data]
        user_dict['achievements'] = [{'title': a['title'], 'description': a['description'], 'type': a['achievement_type'], 'date_earned': a['date_earned'], 'issuer': a['issuer']} for a in achievements_data]
        user_dict['languages'] = [{'name': l['language_name'], 'proficiency': l['proficiency_level']} for l in languages_data]
        
        return user_dict
    finally:
        conn.close()

def update_user_profile(user_id, data):
    conn = get_db_connection()
    try:
        past_projects_json = json.dumps(data.get('past_projects')) if data.get('past_projects') else None
        
        conn.execute('''
            UPDATE users SET 
                name = COALESCE(?, name), bio = COALESCE(?, bio), hall = COALESCE(?, hall),
                branch = COALESCE(?, branch), graduation_year = COALESCE(?, graduation_year),
                current_company = COALESCE(?, current_company), current_position = COALESCE(?, current_position),
                location = COALESCE(?, location), work_preference = COALESCE(?, work_preference),
                phone = COALESCE(?, phone), website = COALESCE(?, website), linkedin = COALESCE(?, linkedin),
                github = COALESCE(?, github), avatar = COALESCE(?, avatar), program = COALESCE(?, program),
                joining_year = COALESCE(?, joining_year), institute = COALESCE(?, institute),
                specialization = COALESCE(?, specialization), past_projects = COALESCE(?, past_projects),
                is_available = COALESCE(?, is_available)
            WHERE id = ?
        ''', (
            data.get('name'), data.get('bio'), data.get('hall'), data.get('branch'), data.get('graduation_year'),
            data.get('current_company'), data.get('current_position'), data.get('location'),
            data.get('work_preference'), data.get('phone'), data.get('website'),
            data.get('linkedin'), data.get('github'), data.get('avatar'),
            data.get('program'), data.get('joining_year'), data.get('institute'),
            data.get('specialization'), past_projects_json, 
            1 if data.get('is_available') else 0 if data.get('is_available') is not None else None,
            user_id
        ))
        
        if 'skills' in data:
            conn.execute('DELETE FROM user_skills WHERE user_id = ?', (user_id,))
            for skill in data['skills']:
                conn.execute('''
                    INSERT INTO user_skills (user_id, skill_name, skill_type, proficiency_level)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, skill.get('name'), skill.get('type', 'technical'), skill.get('proficiency', 'intermediate')))
        
        if 'achievements' in data:
            conn.execute('DELETE FROM user_achievements WHERE user_id = ?', (user_id,))
            for achievement in data['achievements']:
                conn.execute('''
                    INSERT INTO user_achievements (user_id, title, description, achievement_type, date_earned, issuer)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, achievement.get('title'), achievement.get('description'), 
                      achievement.get('type', 'award'), achievement.get('date_earned'), achievement.get('issuer')))
        
        if 'languages' in data:
            conn.execute('DELETE FROM user_languages WHERE user_id = ?', (user_id,))
            for language in data['languages']:
                conn.execute('''
                    INSERT INTO user_languages (user_id, language_name, proficiency_level)
                    VALUES (?, ?, ?)
                ''', (user_id, language.get('name'), language.get('proficiency', 'intermediate')))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_user_avatar(user_id, filename):
    conn = get_db_connection()
    try:
        conn.execute('UPDATE users SET avatar = ? WHERE id = ?', (filename, user_id))
        conn.commit()
    finally:
        conn.close()

def get_user_cv(user_id):
    conn = get_db_connection()
    try:
        res = conn.execute('SELECT cv_pdf FROM users WHERE id = ?', (user_id,)).fetchone()
        return res['cv_pdf'] if res else None
    finally:
        conn.close()

def update_user_cv(user_id, filename):
    conn = get_db_connection()
    try:
        conn.execute('UPDATE users SET cv_pdf = ? WHERE id = ?', (filename, user_id))
        conn.commit()
    finally:
        conn.close()

def clear_user_cv(user_id):
    conn = get_db_connection()
    try:
        conn.execute('UPDATE users SET cv_pdf = NULL WHERE id = ?', (user_id,))
        conn.commit()
    finally:
        conn.close()

def update_student_verification_data(user_id, roll_number=None, id_card_image=None):
    conn = get_db_connection()
    try:
        updates = []
        params = []
        if roll_number is not None:
            updates.append('roll_number = ?')
            params.append(roll_number)
        if id_card_image:
            updates.append('id_card_image = ?')
            params.append(id_card_image)
            
        if not updates:
            return False
            
        params.append(user_id)
        conn.execute(f'UPDATE users SET {", ".join(updates)} WHERE id = ?', params)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_dashboard_stats(user_id, role):
    conn = get_db_connection()
    try:
        if role == 'student':
            mentorship_reqs = conn.execute('SELECT COUNT(*) as c FROM mentorship_requests WHERE student_id = ?', (user_id,)).fetchone()['c']
            pending_allotments = conn.execute('SELECT COUNT(*) as c FROM service_allotments WHERE student_id = ? AND status = "pending_agreement"', (user_id,)).fetchone()['c']
            return {
                'mentorship_requests': mentorship_reqs,
                'pending_service_allotments': pending_allotments
            }
        elif role in ['alumni', 'founder', 'mentor']:
            # Generic stats for advanced user roles since projects/blog are removed
            mentees = conn.execute('SELECT COUNT(*) as c FROM mentorship_requests WHERE alumni_id = ? AND status = "accepted"', (user_id,)).fetchone()['c']
            pending_mentorships = conn.execute('SELECT COUNT(*) as c FROM mentorship_requests WHERE alumni_id = ? AND status = "pending"', (user_id,)).fetchone()['c']
            my_services = conn.execute('SELECT COUNT(*) as c FROM services WHERE provider_id = ?', (user_id,)).fetchone()['c']
            return {
                'mentees': mentees,
                'pending_mentorship_requests': pending_mentorships,
                'active_services': my_services
            }
        else: # investor, admin
            return {}
    finally:
        conn.close()
