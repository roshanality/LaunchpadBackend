import sqlite3
import os

def get_db_path():
    if os.environ.get("RENDER") == "true":  # Running on Render
        base_dir = os.environ.get("RENDER_DATA_DIR", ".")
        return os.path.join(base_dir, "launchpad.db")
    return "launchpad.db"

def get_db_connection():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    # Enable row factory to access columns by name
    conn.row_factory = sqlite3.Row
    return conn
