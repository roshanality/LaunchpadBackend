from database import get_db_connection
from datetime import datetime

def get_services(category=None, search=None):
    conn = get_db_connection()
    try:
        query = '''
            SELECT s.id, s.title, s.description, s.category, s.price_range, s.delivery_time, s.image_url, s.created_at,
                   u.name as provider_name, u.avatar as provider_avatar
            FROM services s
            JOIN users u ON s.provider_id = u.id
            WHERE s.is_active = 1
        '''
        params = []
        if category:
            query += ' AND s.category = ?'
            params.append(category)
        if search:
            query += ' AND (s.title LIKE ? OR s.description LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        query += ' ORDER BY s.created_at DESC'
        
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_service_detail(service_id):
    conn = get_db_connection()
    try:
        row = conn.execute('''
            SELECT s.id, s.title, s.description, s.category, s.price_range, s.delivery_time, s.image_url, s.created_at,
                   u.id as provider_id, u.name as provider_name, u.avatar as provider_avatar, u.bio as provider_bio,
                   u.email as provider_email
            FROM services s
            JOIN users u ON s.provider_id = u.id
            WHERE s.id = ?
        ''', (service_id,)).fetchone()
        
        if not row: return None
        service = {
            'id': row['id'], 'title': row['title'], 'description': row['description'], 'category': row['category'],
            'price_range': row['price_range'], 'delivery_time': row['delivery_time'], 'image_url': row['image_url'], 'created_at': row['created_at'],
            'provider': {
                'id': row['provider_id'], 'name': row['provider_name'], 'avatar': row['provider_avatar'],
                'bio': row['provider_bio'], 'email': row['provider_email']
            }
        }
        
        timeline_rows = conn.execute('SELECT * FROM service_timeline_items WHERE service_id = ? ORDER BY sort_order ASC, date ASC, id ASC', (service_id,)).fetchall()
        service['timeline'] = [dict(r) for r in timeline_rows]
        
        review_rows = conn.execute('SELECT * FROM service_reviews WHERE service_id = ? ORDER BY created_at DESC', (service_id,)).fetchall()
        service['reviews'] = [dict(r) for r in review_rows]
        
        return service
    finally:
        conn.close()

def get_service_timeline(service_id):
    conn = get_db_connection()
    try:
        rows = conn.execute('SELECT * FROM service_timeline_items WHERE service_id = ? ORDER BY sort_order ASC, date ASC, id ASC', (service_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def create_service(user_id, data):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO services (provider_id, title, description, category, price_range, delivery_time, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data['title'], data['description'], data['category'], data.get('price_range'), data.get('delivery_time'), data.get('image_url')))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_my_services(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute('SELECT * FROM services WHERE provider_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def update_service(user_id, service_id, data):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT provider_id FROM services WHERE id = ?', (service_id,)).fetchone()
        if not row: return False, "Not found", 404
        if row['provider_id'] != user_id: return False, "Unauthorized", 403
        
        update_fields = []
        params = []
        for field in ['title', 'description', 'category', 'price_range', 'delivery_time', 'image_url', 'is_active']:
            if field in data:
                update_fields.append(f"{field} = ?")
                params.append(data[field])
        
        if not update_fields: return True, "No fields to update", 200
        
        params.append(service_id)
        conn.execute(f'UPDATE services SET {", ".join(update_fields)} WHERE id = ?', params)
        conn.commit()
        return True, "Success", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_service(user_id, service_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT provider_id FROM services WHERE id = ?', (service_id,)).fetchone()
        if not row: return False, "Not found", 404
        if row['provider_id'] != user_id: return False, "Unauthorized", 403
        
        conn.execute('DELETE FROM services WHERE id = ?', (service_id,))
        conn.commit()
        return True, "Success", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def create_service_request(user_id, data):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO service_requests (user_id, service_id, project_type, description, budget_range)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, data.get('service_id'), data['project_type'], data['description'], data.get('budget_range')))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_admin_service_requests():
    conn = get_db_connection()
    try:
        rows = conn.execute('''
            SELECT sr.*, u.name as user_name, u.email as user_email, u.avatar as user_avatar
            FROM service_requests sr
            JOIN users u ON sr.user_id = u.id
            ORDER BY sr.created_at DESC
        ''').fetchall()
        requests = []
        for r in rows:
            req = dict(r)
            req['user'] = {'id': r['user_id'], 'name': r['user_name'], 'email': r['user_email'], 'avatar': r['user_avatar']}
            requests.append(req)
        return requests
    finally:
        conn.close()

def admin_create_timeline_item(service_id, data):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO service_timeline_items (service_id, title, description, date, image, status, category, sort_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (service_id, data['title'], data['description'], data.get('date'), data.get('image'), data.get('status', 'upcoming'), data.get('category'), data.get('sort_order', 0)))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def admin_update_timeline_item(item_id, data):
    conn = get_db_connection()
    try:
        updates = []
        params = []
        for key in ('title', 'description', 'date', 'image', 'status', 'category', 'sort_order'):
            if key in data:
                updates.append(f'{key} = ?')
                params.append(data[key])
        if not updates: return False, "No fields to update", 400
        params.append(item_id)
        conn.execute(f'UPDATE service_timeline_items SET {", ".join(updates)} WHERE id = ?', params)
        conn.commit()
        return True, "Updated successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def admin_delete_timeline_item(item_id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM service_timeline_items WHERE id = ?', (item_id,))
        conn.commit()
    finally:
        conn.close()

def get_my_service_requests(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute('SELECT * FROM service_requests WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_student_service_profile(user_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT * FROM student_service_profiles WHERE user_id = ?', (user_id,)).fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def upsert_student_service_profile(user_id, data):
    conn = get_db_connection()
    try:
        now = datetime.now().isoformat()
        existing = conn.execute('SELECT id FROM student_service_profiles WHERE user_id = ?', (user_id,)).fetchone()
        if existing:
            conn.execute('''
                UPDATE student_service_profiles SET
                resume_url=?, skills=?, experience=?, education=?, linkedin_url=?, portfolio_url=?, other_info=?, updated_at=?
                WHERE user_id = ?
            ''', (data.get('resume_url'), data.get('skills'), data.get('experience'), data.get('education'), data.get('linkedin_url'), data.get('portfolio_url'), data.get('other_info'), now, user_id))
        else:
            conn.execute('''
                INSERT INTO student_service_profiles (user_id, resume_url, skills, experience, education, linkedin_url, portfolio_url, other_info, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, data.get('resume_url'), data.get('skills'), data.get('experience'), data.get('education'), data.get('linkedin_url'), data.get('portfolio_url'), data.get('other_info'), now))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_my_allotments(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute('''
            SELECT sa.*, s.title as service_title
            FROM service_allotments sa
            JOIN services s ON s.id = sa.service_id
            WHERE sa.student_id = ?
            ORDER BY sa.created_at DESC
        ''', (user_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def create_allotment(service_id, student_id):
    conn = get_db_connection()
    try:
        student = conn.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student')).fetchone()
        if not student: return False, "Invalid student", 400
        service = conn.execute('SELECT id FROM services WHERE id = ?', (service_id,)).fetchone()
        if not service: return False, "Invalid service", 400
        existing = conn.execute('SELECT id FROM service_allotments WHERE service_id = ? AND student_id = ?', (service_id, student_id)).fetchone()
        if existing: return False, "Student already allotted to this service", 400
        
        conn.execute('INSERT INTO service_allotments (service_id, student_id, status) VALUES (?, ?, ?)', (service_id, student_id, 'pending_agreement'))
        conn.commit()
        return True, "Created", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def agree_allotment(user_id, allotment_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT id, status FROM service_allotments WHERE id = ? AND student_id = ?', (allotment_id, user_id)).fetchone()
        if not row: return False, "Allotment not found", 404
        if row['status'] != 'pending_agreement': return False, "Already responded to this allotment", 400
        
        now = datetime.now().isoformat()
        conn.execute('UPDATE service_allotments SET status = ?, agreed_at = ? WHERE id = ?', ('agreed', now, allotment_id))
        conn.commit()
        return True, "Success", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def is_admin(user_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        return row and row['role'] == 'admin'
    finally:
        conn.close()

def is_student(user_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        return row and row['role'] == 'student'
    finally:
        conn.close()
