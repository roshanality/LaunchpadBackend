#!/usr/bin/env python3
"""
Script to add feedback columns to the project_applications table
Run this if you're getting "invalid action" errors when marking projects as completed
"""

import sqlite3

def add_feedback_columns():
    conn = sqlite3.connect('launchpad.db')
    cursor = conn.cursor()
    
    try:
        print("Adding feedback columns to project_applications table...")
        
        # Add feedback column
        try:
            cursor.execute('ALTER TABLE project_applications ADD COLUMN feedback TEXT')
            print("✓ Added 'feedback' column")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("✓ 'feedback' column already exists")
            else:
                print(f"✗ Error adding 'feedback' column: {e}")
        
        # Add completed_at column
        try:
            cursor.execute('ALTER TABLE project_applications ADD COLUMN completed_at TIMESTAMP')
            print("✓ Added 'completed_at' column")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("✓ 'completed_at' column already exists")
            else:
                print(f"✗ Error adding 'completed_at' column: {e}")
        
        # Add is_completed column
        try:
            cursor.execute('ALTER TABLE project_applications ADD COLUMN is_completed BOOLEAN DEFAULT 0')
            print("✓ Added 'is_completed' column")
        except sqlite3.OperationalError as e:
            if 'duplicate column name' in str(e).lower():
                print("✓ 'is_completed' column already exists")
            else:
                print(f"✗ Error adding 'is_completed' column: {e}")
        
        conn.commit()
        print("\n✅ Database schema updated successfully!")
        print("You can now mark projects as completed.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    add_feedback_columns()
