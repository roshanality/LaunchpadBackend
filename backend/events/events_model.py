from database import get_db_connection

def is_admin(user_id):
    conn = get_db_connection()
    try:
        row = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        return row and row['role'] == 'admin'
    finally:
        conn.close()

def get_user_enrolled_events(user_id):
    conn = get_db_connection()
    try:
        rows = conn.execute('''
            SELECT e.id, e.title, e.description, e.type, e.date, e.time, e.location, e.image_url,
                   e.speaker_name, ee.enrolled_at
            FROM event_enrollments ee
            JOIN events e ON ee.event_id = e.id
            WHERE ee.user_id = ?
            ORDER BY e.date DESC
        ''', (user_id,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_events(user_id=None):
    conn = get_db_connection()
    try:
        query = '''
            SELECT e.id, e.title, e.description, e.type, e.date, e.time, e.location, e.image_url, e.created_at,
                   e.speaker_name, e.speaker_bio, e.speaker_image, e.speaker_contact,
                   (SELECT COUNT(*) FROM event_enrollments WHERE event_id = e.id) as attendee_count,
                   CASE WHEN ? IS NOT NULL THEN (SELECT 1 FROM event_enrollments WHERE event_id = e.id AND user_id = ?) ELSE 0 END as is_enrolled
            FROM events e
            ORDER BY e.date ASC
        '''
        rows = conn.execute(query, (user_id, user_id)).fetchall()
        
        events = []
        for r in rows:
            event = dict(r)
            event['is_enrolled'] = bool(event['is_enrolled'])
            events.append(event)
        return events
    finally:
        conn.close()

def get_event(event_id, user_id=None):
    conn = get_db_connection()
    try:
        row = conn.execute('''
            SELECT e.id, e.title, e.description, e.type, e.date, e.time, e.location, e.image_url, e.created_at,
                   e.speaker_name, e.speaker_bio, e.speaker_image, e.speaker_contact,
                   (SELECT COUNT(*) FROM event_enrollments WHERE event_id = e.id) as attendee_count,
                   CASE WHEN ? IS NOT NULL THEN (SELECT 1 FROM event_enrollments WHERE event_id = e.id AND user_id = ?) ELSE 0 END as is_enrolled
            FROM events e
            WHERE e.id = ?
        ''', (user_id, user_id, event_id)).fetchone()
        
        if not row: return None
        event = dict(row)
        event['is_enrolled'] = bool(event['is_enrolled'])
        return event
    finally:
        conn.close()

def create_event(user_id, data):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin access required", 403
            
        required = ['title', 'description', 'type', 'date', 'time']
        for field in required:
            if not data.get(field): return None, f'{field} is required', 400
                 
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (title, description, type, date, time, location, image_url, speaker_name, speaker_bio, speaker_image, speaker_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['title'], data['description'], data['type'], data['date'], data['time'],
            data.get('location'), data.get('image_url'), data.get('speaker_name'),
            data.get('speaker_bio'), data.get('speaker_image'), data.get('speaker_contact')
        ))
        conn.commit()
        return cursor.lastrowid, "Event created successfully", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_event(user_id, event_id, data):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return False, "Admin access required", 403
            
        fields = []
        values = []
        allowed = ['title', 'description', 'type', 'date', 'time', 'location', 'image_url', 'speaker_name', 'speaker_bio', 'speaker_image', 'speaker_contact']
        
        for field in allowed:
            if field in data:
                fields.append(f"{field} = ?")
                values.append(data[field])
                
        if not fields: return True, "No changes", 200
            
        values.append(event_id)
        conn.execute(f"UPDATE events SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
        return True, "Event updated successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def enroll_event(user_id, event_id):
    conn = get_db_connection()
    try:
        existing = conn.execute('SELECT id FROM event_enrollments WHERE user_id = ? AND event_id = ?', (user_id, event_id)).fetchone()
        if existing: return False, "Already enrolled", 400
            
        conn.execute('INSERT INTO event_enrollments (user_id, event_id) VALUES (?, ?)', (user_id, event_id))
        conn.commit()
        return True, "Enrolled successfully", 201
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_event_attendees(user_id, event_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return None, "Admin access required", 403
            
        rows = conn.execute('''
            SELECT u.id, u.name, u.email, u.avatar, ee.enrolled_at
            FROM event_enrollments ee
            JOIN users u ON ee.user_id = u.id
            WHERE ee.event_id = ?
            ORDER BY ee.enrolled_at DESC
        ''', (event_id,)).fetchall()
        return [dict(r) for r in rows], None, 200
    finally:
        conn.close()

def delete_event(user_id, event_id):
    conn = get_db_connection()
    try:
        if not is_admin(user_id): return False, "Admin access required", 403
            
        conn.execute('DELETE FROM event_enrollments WHERE event_id = ?', (event_id,))
        conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
        conn.commit()
        return True, "Event deleted successfully", 200
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
