from database import get_db_connection, get_db_path
import sqlite3
import random
import string
from datetime import datetime, timedelta

def _ensure_reset_columns():
    """Add password reset columns if they don't exist (safe to call on every boot)."""
    conn = sqlite3.connect(get_db_path())
    for col, typedef in [('reset_token', 'TEXT'), ('reset_token_expires', 'TEXT')]:
        try:
            conn.execute(f'ALTER TABLE users ADD COLUMN {col} {typedef}')
        except Exception:
            pass
    conn.commit()
    conn.close()

_ensure_reset_columns()


def _ensure_otp_table():
    conn = sqlite3.connect(get_db_path())
    conn.execute('''
        CREATE TABLE IF NOT EXISTS admin_otps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            otp TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

_ensure_otp_table()


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def save_admin_otp(user_id, otp):
    expires_at = (datetime.utcnow() + timedelta(minutes=5)).isoformat()
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO admin_otps (user_id, otp, expires_at) VALUES (?, ?, ?) '
            'ON CONFLICT(user_id) DO UPDATE SET otp = excluded.otp, expires_at = excluded.expires_at, created_at = CURRENT_TIMESTAMP',
            (user_id, otp, expires_at)
        )
        conn.commit()
    finally:
        conn.close()


def verify_admin_otp(user_id, otp):
    """Returns True if OTP matches and is not expired, then deletes it."""
    conn = get_db_connection()
    try:
        row = conn.execute(
            'SELECT otp, expires_at FROM admin_otps WHERE user_id = ?', (user_id,)
        ).fetchone()
        if not row:
            return False
        if row['otp'] != otp:
            return False
        if datetime.utcnow() > datetime.fromisoformat(row['expires_at']):
            return False
        conn.execute('DELETE FROM admin_otps WHERE user_id = ?', (user_id,))
        conn.commit()
        return True
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = get_db_connection()
    try:
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()


def create_user(user_data):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, password_hash, role, graduation_year, department, is_approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['name'],
            user_data['email'],
            user_data['password_hash'],
            user_data['role'],
            user_data.get('graduation_year'),
            user_data.get('department'),
            user_data.get('is_approved', True)
        ))
        conn.commit()
        user_id = cursor.lastrowid
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()


def set_reset_token(user_id, token, expires_at):
    conn = get_db_connection()
    try:
        conn.execute(
            'UPDATE users SET reset_token = ?, reset_token_expires = ? WHERE id = ?',
            (token, expires_at, user_id)
        )
        conn.commit()
    finally:
        conn.close()


def get_user_by_reset_token(token):
    conn = get_db_connection()
    try:
        user = conn.execute(
            'SELECT * FROM users WHERE reset_token = ?', (token,)
        ).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()


def update_password(user_id, password_hash):
    conn = get_db_connection()
    try:
        conn.execute(
            'UPDATE users SET password_hash = ?, reset_token = NULL, reset_token_expires = NULL WHERE id = ?',
            (password_hash, user_id)
        )
        conn.commit()
    finally:
        conn.close()
