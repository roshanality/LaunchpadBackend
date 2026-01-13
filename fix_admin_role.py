#!/usr/bin/env python3
"""
Fix the users table to allow 'admin' role
"""
import sqlite3
import os

def fix_admin_role():
    db_path = "launchpad.db"
    if os.environ.get("RENDER") == "true":
        base_dir = os.environ.get("RENDER_DATA_DIR", ".")
        db_path = os.path.join(base_dir, "launchpad.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # SQLite doesn't support ALTER TABLE to modify CHECK constraints
        # We need to recreate the table
        
        # Step 1: Create a new table with the correct constraint
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('student', 'alumni', 'admin')),
                graduation_year INTEGER,
                department TEXT,
                hall TEXT,
                branch TEXT,
                bio TEXT,
                current_company TEXT,
                current_position TEXT,
                location TEXT,
                work_preference TEXT CHECK (work_preference IN ('onsite', 'remote', 'hybrid')),
                phone TEXT,
                website TEXT,
                linkedin TEXT,
                github TEXT,
                avatar TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                years_of_experience INTEGER,
                domain TEXT,
                tech_skills TEXT,
                program TEXT,
                cv_pdf TEXT,
                joining_year INTEGER,
                institute TEXT,
                specialization TEXT,
                past_projects TEXT,
                is_available BOOLEAN DEFAULT 1,
                is_approved BOOLEAN DEFAULT 1
            )
        ''')
        
        # Step 2: Copy all data from old table to new table
        cursor.execute('''
            INSERT INTO users_new 
            SELECT 
                id, name, email, password_hash, role, graduation_year, department,
                hall, branch, bio, current_company, current_position, location,
                work_preference, phone, website, linkedin, github, avatar,
                created_at, years_of_experience, domain, tech_skills, program,
                cv_pdf, joining_year, institute, specialization, past_projects,
                is_available,
                CASE WHEN is_approved IS NULL THEN 1 ELSE is_approved END as is_approved
            FROM users
        ''')
        
        # Step 3: Drop old table
        cursor.execute('DROP TABLE users')
        
        # Step 4: Rename new table
        cursor.execute('ALTER TABLE users_new RENAME TO users')
        
        # Step 5: Recreate indexes and foreign key constraints if needed
        # (Add any indexes that were on the old table)
        
        conn.commit()
        print("✓ Successfully updated users table to allow 'admin' role")
        
        # Verify
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        if result and 'admin' in result[0]:
            print("✓ Verified: 'admin' role is now allowed in the constraint")
        else:
            print("⚠ Warning: Could not verify constraint update")
            
    except Exception as e:
        conn.rollback()
        print(f"✗ Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    fix_admin_role()
