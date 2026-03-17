from database import get_db_connection

def is_admin(user_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        return row and row['role'] == 'admin'
    finally:
        conn.close()

def get_admin_id(conn):
    admin_result = conn.execute('SELECT id FROM users WHERE role = ?', ('admin',)).fetchone()
    return admin_result['id'] if admin_result else None

def get_support_messages(user_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Unauthorized", 403
        
        admin_id = get_admin_id(conn)
        if not admin_id: return None, "Admin user not found", 404
        
        rows = conn.execute('''
            SELECT c.id, c.user1_id, c.user2_id, c.created_at, c.updated_at,
                   CASE WHEN c.user1_id = ? THEN u2.name ELSE u1.name END as user_name,
                   CASE WHEN c.user1_id = ? THEN u2.email ELSE u1.email END as user_email,
                   CASE WHEN c.user1_id = ? THEN c.user2_id ELSE c.user1_id END as other_user_id
            FROM conversations c
            LEFT JOIN users u1 ON c.user1_id = u1.id
            LEFT JOIN users u2 ON c.user2_id = u2.id
            WHERE (c.user1_id = ? OR c.user2_id = ?)
            ORDER BY c.updated_at DESC
        ''', (admin_id, admin_id, admin_id, admin_id, admin_id)).fetchall()
        
        conversations = []
        for row in rows:
            last_msg = conn.execute('''
                SELECT content, created_at FROM messages
                WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
                ORDER BY created_at DESC LIMIT 1
            ''', (row['user1_id'], row['user2_id'], row['user2_id'], row['user1_id'])).fetchone()
            
            unread = conn.execute('''
                SELECT COUNT(*) as c FROM messages
                WHERE ((sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?))
                AND is_read = 0 AND receiver_id = ?
            ''', (row['user1_id'], row['user2_id'], row['user2_id'], row['user1_id'], admin_id)).fetchone()['c']
            
            conversations.append({
                'id': row['id'],
                'user_id': row['other_user_id'],
                'user_name': row['user_name'],
                'user_email': row['user_email'],
                'last_message': last_msg['content'] if last_msg else None,
                'last_message_time': last_msg['created_at'] if last_msg else row['updated_at'],
                'unread_count': unread,
                'created_at': row['created_at']
            })
        return conversations, None, 200
    finally:
        conn.close()

def send_support_message(user_id, content):
    conn = get_db_connection()
    try:
        admin_id = get_admin_id(conn)
        if not admin_id: return False, "Admin user not found", 404
        
        conv = conn.execute('''
            SELECT id FROM conversations
            WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
        ''', (user_id, admin_id, admin_id, user_id)).fetchone()
        
        if not conv:
            conn.execute('''
                INSERT INTO conversations (user1_id, user2_id, created_at, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (user_id, admin_id))
        else:
            conn.execute('UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?', (conv['id'],))
            
        conn.execute('''
            INSERT INTO messages (sender_id, receiver_id, content, created_at, is_read)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, 0)
        ''', (user_id, admin_id, content))
        
        conn.commit()
        return True, "Support message sent successfully", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_conversations(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute('''
            SELECT DISTINCT 
                CASE WHEN user1_id = ? THEN user2_id ELSE user1_id END as other_user_id,
                u.name as other_user_name, u.email as other_user_email,
                u.role as other_user_role, u.avatar as other_user_avatar
            FROM conversations c
            JOIN users u ON u.id = CASE WHEN c.user1_id = ? THEN c.user2_id ELSE c.user1_id END
            WHERE c.user1_id = ? OR c.user2_id = ?
            ORDER BY c.updated_at DESC
        ''', (user_id, user_id, user_id, user_id)).fetchall()
        
        conversations = []
        for row in rows:
            other_id = row['other_user_id']
            last_msg = conn.execute('''
                SELECT content, created_at FROM messages
                WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
                ORDER BY created_at DESC LIMIT 1
            ''', (user_id, other_id, other_id, user_id)).fetchone()
            
            unread = conn.execute('''
                SELECT COUNT(*) as c FROM messages WHERE sender_id = ? AND receiver_id = ? AND is_read = 0
            ''', (other_id, user_id)).fetchone()['c']
            
            conv = conn.execute('''
                SELECT id FROM conversations WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
            ''', (user_id, other_id, other_id, user_id)).fetchone()
            
            conversations.append({
                'id': conv['id'] if conv else None,
                'other_user_id': other_id,
                'other_user_name': row['other_user_name'],
                'other_user_email': row['other_user_email'],
                'other_user_role': row['other_user_role'],
                'other_user_avatar': row['other_user_avatar'],
                'last_message': last_msg['content'] if last_msg else None,
                'last_message_time': last_msg['created_at'] if last_msg else None,
                'unread_count': unread,
                'is_online': False
            })
        return conversations
    finally:
        conn.close()

def create_conversation(user_id, other_user_id):
    conn = get_db_connection()
    try:
        existing = conn.execute('''
            SELECT id FROM conversations WHERE (user1_id = ? AND user2_id = ?) OR (user1_id = ? AND user2_id = ?)
        ''', (user_id, other_user_id, other_user_id, user_id)).fetchone()
        
        if existing: return existing['id']
            
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (user1_id, user2_id, created_at, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', (min(user_id, other_user_id), max(user_id, other_user_id)))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_conversation(user_id, conv_id):
    conn = get_db_connection()
    try:
        conv = conn.execute('SELECT user1_id, user2_id FROM conversations WHERE id = ?', (conv_id,)).fetchone()
        if not conv: return None, "Conversation not found", 404
        if user_id not in [conv['user1_id'], conv['user2_id']]: return None, "Access denied", 403
            
        other_id = conv['user2_id'] if conv['user1_id'] == user_id else conv['user1_id']
        u = conn.execute('SELECT id, name, email, role, department, graduation_year FROM users WHERE id = ?', (other_id,)).fetchone()
        if not u: return None, "User not found", 404
            
        return {
            'id': u['id'], 'name': u['name'], 'email': u['email'], 'role': u['role'],
            'department': u['department'], 'graduation_year': u['graduation_year'], 'is_online': False
        }, None, 200
    finally:
        conn.close()

def get_messages(user_id, conv_id):
    conn = get_db_connection()
    try:
        conv = conn.execute('SELECT user1_id, user2_id FROM conversations WHERE id = ?', (conv_id,)).fetchone()
        if not conv or user_id not in [conv['user1_id'], conv['user2_id']]: return None, "Access denied", 403
            
        rows = conn.execute('''
            SELECT id, sender_id, receiver_id, content, created_at, is_read FROM messages
            WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ORDER BY created_at ASC
        ''', (conv['user1_id'], conv['user2_id'], conv['user2_id'], conv['user1_id'])).fetchall()
        
        conn.execute('UPDATE messages SET is_read = 1 WHERE receiver_id = ? AND is_read = 0', (user_id,))
        conn.commit()
        
        msgs = []
        for r in rows:
            m = dict(r)
            m['is_read'] = bool(m['is_read'])
            msgs.append(m)
        return msgs, None, 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def send_message(user_id, conv_id, content):
    conn = get_db_connection()
    try:
        conv = conn.execute('SELECT user1_id, user2_id FROM conversations WHERE id = ?', (conv_id,)).fetchone()
        if not conv or user_id not in [conv['user1_id'], conv['user2_id']]: return None, "Access denied", 403
            
        receiver_id = conv['user2_id'] if conv['user1_id'] == user_id else conv['user1_id']
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (sender_id, receiver_id, content, created_at, is_read)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, 0)
        ''', (user_id, receiver_id, content))
        msg_id = cursor.lastrowid
        
        conn.execute('UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?', (conv_id,))
        conn.commit()
        
        new_msg = conn.execute('SELECT * FROM messages WHERE id = ?', (msg_id,)).fetchone()
        m = dict(new_msg)
        m['is_read'] = bool(m['is_read'])
        return m, None, 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_available_users(user_id):
    conn = get_db_connection()
    try:
        role = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()['role']
        if role == 'student':
            rows = conn.execute('''
                SELECT id, name, email, role, department, graduation_year, current_company, current_position, location, bio, linkedin, github, website, hall, branch, avatar
                FROM users WHERE id != ? AND role = 'student' ORDER BY name
            ''', (user_id,)).fetchall()
        else:
            rows = conn.execute('''
                SELECT id, name, email, role, department, graduation_year, current_company, current_position, location, bio, linkedin, github, website, hall, branch, avatar
                FROM users WHERE id != ? ORDER BY name
            ''', (user_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ── Notifications ─────────────────────────────────────────────────────────────

def _ensure_notifications_table():
    from database import get_db_path
    import sqlite3
    conn = sqlite3.connect(get_db_path())
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT DEFAULT 'info',
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

_ensure_notifications_table()


def get_notifications(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM user_notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 50',
            (user_id,)
        ).fetchall()
        result = []
        for r in rows:
            n = dict(r)
            n['is_read'] = bool(n['is_read'])
            result.append(n)
        return result
    finally:
        conn.close()


def create_notification(user_id, message, notif_type='info'):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO user_notifications (user_id, type, message) VALUES (?, ?, ?)',
            (user_id, notif_type, message)
        )
        conn.commit()
        row = conn.execute('SELECT * FROM user_notifications WHERE id = ?', (cursor.lastrowid,)).fetchone()
        n = dict(row)
        n['is_read'] = bool(n['is_read'])
        return n
    finally:
        conn.close()


def mark_notification_read(user_id, notif_id):
    conn = get_db_connection()
    try:
        conn.execute(
            'UPDATE user_notifications SET is_read = 1 WHERE id = ? AND user_id = ?',
            (notif_id, user_id)
        )
        conn.commit()
    finally:
        conn.close()


def delete_notification(user_id, notif_id):
    conn = get_db_connection()
    try:
        conn.execute(
            'DELETE FROM user_notifications WHERE id = ? AND user_id = ?',
            (notif_id, user_id)
        )
        conn.commit()
    finally:
        conn.close()
