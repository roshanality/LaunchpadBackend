#!/usr/bin/env python3
"""
Test script to create admin user and test admin login
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import init_db, init_admin, get_db_path
import sqlite3

def test_admin_setup():
    print("Initializing database...")
    init_db()
    
    print("Creating admin user...")
    init_admin()
    
    # Verify admin user exists
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name, email, role, is_approved FROM users WHERE email = ?', ('Admin@kgplaunchpad.in',))
    result = cursor.fetchone()
    
    if result:
        print(f"\n✓ Admin user found:")
        print(f"  ID: {result[0]}")
        print(f"  Name: {result[1]}")
        print(f"  Email: {result[2]}")
        print(f"  Role: {result[3]}")
        print(f"  Approved: {result[4]}")
    else:
        print("\n✗ Admin user not found!")
    
    conn.close()
    print("\nAdmin setup complete!")

if __name__ == '__main__':
    test_admin_setup()
