from database import get_db_connection

def is_admin(user_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        return row and row['role'] == 'admin'
    finally:
        conn.close()

def get_resources(category=None, search=None):
    conn = get_db_connection()
    try:
        query = 'SELECT id, title, description, category, link, image_url, created_at FROM resources WHERE 1=1'
        params = []
        if category:
            query += ' AND category = ?'
            params.append(category)
        if search:
            query += ' AND (title LIKE ? OR description LIKE ?)'
            params.append(f'%{search}%')
            params.append(f'%{search}%')
            
        query += ' ORDER BY created_at DESC'
        
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def create_resource(user_id, data):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Unauthorized", 403
            
        required = ['title', 'description', 'category']
        for field in required:
            if not data.get(field): return None, f'{field} is required', 400
            
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO resources (title, description, category, link, image_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['title'], data['description'], data['category'], data.get('link'), data.get('image_url')))
        
        resource_id = cursor.lastrowid
        conn.commit()
        return resource_id, "Resource created successfully", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_resource(user_id, resource_id, data):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return False, "Unauthorized", 403
            
        required = ['title', 'description', 'category']
        for field in required:
            if not data.get(field): return False, f'{field} is required', 400
            
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE resources
            SET title = ?, description = ?, category = ?, link = ?, image_url = ?
            WHERE id = ?
        ''', (data['title'], data['description'], data['category'], data.get('link'), data.get('image_url'), resource_id))
        
        if cursor.rowcount == 0: return False, "Resource not found", 404
            
        conn.commit()
        return True, "Resource updated successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_resource(user_id, resource_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return False, "Unauthorized", 403
            
        cursor = conn.cursor()
        cursor.execute('DELETE FROM resources WHERE id = ?', (resource_id,))
        if cursor.rowcount == 0: return False, "Resource not found", 404
            
        conn.commit()
        return True, "Resource deleted successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
