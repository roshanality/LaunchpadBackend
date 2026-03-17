from database import get_db_connection

def is_admin(user_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        return row and row['role'] == 'admin'
    finally:
        conn.close()

def get_courses(search=None, category=None):
    conn = get_db_connection()
    try:
        query = '''
            SELECT id, title, description, category, image_url, price, duration, start_date, created_at,
                   instructor_name, instructor_image, skill_tags, lessons_count 
            FROM courses WHERE 1=1
        '''
        params = []
        if search:
            query += ' AND (title LIKE ? OR description LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        if category:
            query += ' AND category = ?'
            params.append(category)
            
        query += ' ORDER BY created_at DESC'
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_course_detail(course_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def create_course(user_id, data):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin access required", 403
        
        for field in ['title', 'description', 'category']:
            if not data.get(field): return None, f'{field} is required', 400
            
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO courses (title, description, perks, timeline, duration, assignments, category, image_url, price, start_date,
                                instructor_name, instructor_bio, instructor_image, what_you_learn, requirements, lessons, skill_tags, lessons_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['title'], data['description'], data.get('perks'), data.get('timeline'), data.get('duration'),
            data.get('assignments'), data['category'], data.get('image_url'), data.get('price'), data.get('start_date'),
            data.get('instructor_name'), data.get('instructor_bio'), data.get('instructor_image'), data.get('what_you_learn'),
            data.get('requirements'), data.get('lessons'), data.get('skill_tags'), data.get('lessons_count', 0)
        ))
        conn.commit()
        return cursor.lastrowid, "Course created successfully", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_course(user_id, course_id, data):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return False, "Admin access required", 403
        
        course = conn.execute("SELECT id FROM courses WHERE id = ?", (course_id,)).fetchone()
        if not course: return False, "Course not found", 404
        
        fields = []
        values = []
        allowed = ['title', 'description', 'perks', 'timeline', 'duration', 'assignments', 'category', 'image_url', 'price', 'start_date',
                   'instructor_name', 'instructor_bio', 'instructor_image', 'what_you_learn', 'requirements', 'lessons', 'skill_tags', 'lessons_count']
        
        for field in allowed:
            if field in data:
                fields.append(f"{field} = ?")
                values.append(data[field])
                
        if not fields: return True, "No changes provided", 200
        
        values.append(course_id)
        conn.execute(f"UPDATE courses SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
        return True, "Course updated successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def enroll_course(user_id, course_id):
    conn = get_db_connection()
    try:
        course = conn.execute('SELECT id FROM courses WHERE id = ?', (course_id,)).fetchone()
        if not course: return False, "Course not found", 404
        
        existing = conn.execute('SELECT id FROM course_enrollments WHERE user_id = ? AND course_id = ?', (user_id, course_id)).fetchone()
        if existing: return False, "Already enrolled in this course", 400
        
        conn.execute('''
            INSERT INTO course_enrollments (user_id, course_id, status, payment_status)
            VALUES (?, ?, 'pending', 'paid') 
        ''', (user_id, course_id))
        conn.commit()
        return True, "Enrolled successfully", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_admin_courses(user_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin access required", 403
        
        rows = conn.execute('''
            SELECT c.id, c.title, c.category, c.created_at, COUNT(ce.id) as enrollment_count
            FROM courses c
            LEFT JOIN course_enrollments ce ON c.id = ce.course_id
            GROUP BY c.id
            ORDER BY c.created_at DESC
        ''').fetchall()
        return [dict(r) for r in rows], None, 200
    finally:
        conn.close()

def get_course_students(user_id, course_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin access required", 403
        
        rows = conn.execute('''
            SELECT ce.id, ce.user_id, ce.status, ce.payment_status, ce.enrolled_at,
                   u.name, u.email, u.avatar
            FROM course_enrollments ce
            JOIN users u ON ce.user_id = u.id
            WHERE ce.course_id = ?
            ORDER BY ce.enrolled_at DESC
        ''', (course_id,)).fetchall()
        return [dict(r) for r in rows], None, 200
    finally:
        conn.close()

def get_user_enrolled_courses(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute('''
            SELECT c.id, c.title, c.description, c.category, c.image_url, c.duration, c.instructor_name, c.instructor_image,
                   ce.status as enrollment_status, ce.enrolled_at
            FROM course_enrollments ce
            JOIN courses c ON ce.course_id = c.id
            WHERE ce.user_id = ?
            ORDER BY ce.enrolled_at DESC
        ''', (user_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
