#!/usr/bin/env python3
"""
Create admin user in the database
"""
import sqlite3
import os
import sys

# Try to import werkzeug, if not available, we'll use a workaround
try:
    from werkzeug.security import generate_password_hash
    HAS_WERKZEUG = True
except ImportError:
    HAS_WERKZEUG = False
    print("Warning: werkzeug not available, will need to use app's function")

def create_admin_user():
    db_path = "launchpad.db"
    if os.environ.get("RENDER") == "true":
        base_dir = os.environ.get("RENDER_DATA_DIR", ".")
        db_path = os.path.join(base_dir, "launchpad.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if admin already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', ('Admin@kgplaunchpad.in',))
        if cursor.fetchone():
            print("Admin user already exists")
            return
        
        if HAS_WERKZEUG:
            password_hash = generate_password_hash('IITKGP2026')
        else:
            # If werkzeug is not available, try to import from app
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            try:
                from werkzeug.security import generate_password_hash
                password_hash = generate_password_hash('IITKGP2026')
            except:
                print("Error: Cannot generate password hash. Please install werkzeug or run the app to create admin user.")
                return
        
        # Create admin user
        cursor.execute('''
            INSERT INTO users (name, email, password_hash, role, is_approved)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Admin', 'Admin@kgplaunchpad.in', password_hash, 'admin', True))
        
        conn.commit()
        print("✓ Admin user created successfully")
        
        # Verify
        cursor.execute('SELECT id, name, email, role, is_approved FROM users WHERE email = ?', ('Admin@kgplaunchpad.in',))
        result = cursor.fetchone()
        if result:
            print(f"✓ Admin user verified:")
            print(f"  ID: {result[0]}")
            print(f"  Name: {result[1]}")
            print(f"  Email: {result[2]}")
            print(f"  Role: {result[3]}")
            print(f"  Approved: {result[4]}")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error creating admin user: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    create_admin_user()
