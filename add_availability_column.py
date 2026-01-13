import sqlite3
import os

def add_availability_column():
    """Add is_available column to users table"""
    
    # Determine database path
    if os.environ.get("RENDER") == "true":
        base_dir = os.environ.get("RENDER_DATA_DIR", ".")
        db_path = os.path.join(base_dir, "launchpad.db")
    else:
        db_path = "launchpad.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add is_available column if it doesn't exist
        cursor.execute('ALTER TABLE users ADD COLUMN is_available BOOLEAN DEFAULT 1')
        print("✓ Added is_available column to users table")
        
        # Set all existing alumni to available by default
        cursor.execute("UPDATE users SET is_available = 1 WHERE role = 'alumni' AND is_available IS NULL")
        print("✓ Set all existing alumni to available")
        
        conn.commit()
        print("\n✅ Successfully added availability feature!")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("ℹ️  Column is_available already exists")
        else:
            print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    add_availability_column()
