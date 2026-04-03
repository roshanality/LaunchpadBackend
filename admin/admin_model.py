from database import get_db_connection

def is_admin(user_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        return row and row['role'] == 'admin'
    finally:
        conn.close()

def get_admin_student_verifications(user_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin access required", 403
            
        rows = conn.execute('''
            SELECT id, name, email, role, roll_number, id_card_image, graduation_year, department
            FROM users
            WHERE role = 'student' AND ((roll_number IS NOT NULL AND roll_number != '') OR (id_card_image IS NOT NULL AND id_card_image != ''))
            ORDER BY name
        ''').fetchall()
        
        result = []
        for row in rows:
            r = dict(row)
            r['roll_number'] = r['roll_number'] or ''
            r['id_card_image'] = r['id_card_image'] or ''
            r['department'] = r['department'] or ''
            result.append(r)
        return result, None, 200
    finally:
        conn.close()

def get_pending_users(user_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Unauthorized", 403
            
        rows = conn.execute('''
            SELECT id, name, email, role, graduation_year, department, created_at
            FROM users
            WHERE role IN ('alumni', 'founder', 'mentor', 'investor') AND (is_approved IS NULL OR is_approved = 0)
            ORDER BY created_at DESC
        ''').fetchall()
        return [dict(r) for r in rows], None, 200
    finally:
        conn.close()

def approve_user(admin_id, target_id):
    conn = get_db_connection()
    try:
        if not is_admin(admin_id): return False, "Unauthorized", 403
            
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET is_approved = 1
            WHERE id = ? AND role IN ('alumni', 'founder', 'mentor', 'investor')
        ''', (target_id,))
        if cursor.rowcount == 0: return False, "User not found or role doesn't require approval", 404
            
        conn.commit()
        return True, "User approved successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def reject_user(admin_id, target_id):
    conn = get_db_connection()
    try:
        if not is_admin(admin_id): return False, "Unauthorized", 403
            
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET is_approved = 0
            WHERE id = ? AND role IN ('alumni', 'founder', 'mentor', 'investor')
        ''', (target_id,))
        if cursor.rowcount == 0: return False, "User not found or role doesn't require approval", 404
            
        conn.commit()
        return True, "User rejected successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_admin_stats(user_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin access required", 403
            
        students_count = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'student'").fetchone()[0]
        alumni_count = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'alumni'").fetchone()[0]
        courses_count = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
        
        # We drop projects, so this is hardcoded for now or we just skip it
        active_projects = 0
        
        stats = [
            {'key': 'courses_count', 'label': 'Courses', 'value': f"{courses_count}+"},
            {'key': 'students_count', 'label': 'Students', 'value': f"{students_count}+"},
            {'key': 'alumni_count', 'label': 'Alumni Worldwide', 'value': f"{alumni_count}+"},
            {'key': 'instructors_count', 'label': 'Expert Instructors', 'value': "150+"},
            {'key': 'satisfaction_rate', 'label': 'Satisfaction Rate', 'value': "98%"},
            {'key': 'years_excellence', 'label': 'Years of Excellence', 'value': "75+"},
            {'key': 'success_stories', 'label': 'Success Stories', 'value': "200+"}
        ]
        return stats, None, 200
    finally:
        conn.close()

def update_admin_stat(user_id, data):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin access required", 403
            
        key, label, value = data.get('key'), data.get('label'), data.get('value')
        if not key or not label or not value: return None, "Missing fields", 400
            
        conn.execute('''
            INSERT INTO site_stats (key, label, value, updated_at) 
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(key) DO UPDATE SET label=excluded.label, value=excluded.value, updated_at=CURRENT_TIMESTAMP
        ''', (key, label, value))
        conn.commit()
        return {'key': key, 'label': label, 'value': value}, None, 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_all_users_admin(user_id, role_filter=None):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin access required", 403
            
        query = 'SELECT id, name, email, role, is_approved, is_blocked, created_at, avatar, alumni_type FROM users'
        params = []
        if role_filter:
            query += ' WHERE role = ?'
            params.append(role_filter)
        query += ' ORDER BY created_at DESC'
        
        rows = conn.execute(query, params).fetchall()
        result = []
        for row in rows:
            r = dict(row)
            r['is_approved'] = bool(r['is_approved'])
            r['is_blocked'] = bool(r['is_blocked'])
            result.append(r)
        return result, None, 200
    finally:
        conn.close()

def toggle_block_user(admin_id, target_id, should_block):
    conn = get_db_connection()
    try:
        if not is_admin(admin_id): return False, "Admin access required", 403
        if admin_id == target_id: return False, "Cannot block yourself", 400
            
        conn.execute('UPDATE users SET is_blocked = ? WHERE id = ?', (should_block, target_id))
        conn.commit()
        return True, f"User {'blocked' if should_block else 'unblocked'} successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
