"""
Migration script for Railway deployment - Make image_path optional in glimpse table
Run this on Railway after deployment
"""
import sqlite3
import os
from pathlib import Path

def migrate_database():
    # Find the database file
    possible_paths = [
        'backend/instance/university.db',
        'instance/university.db',
        'university.db'
    ]
    
    db_path = None
    for path in possible_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("Database not found. Creating new database with correct schema.")
        # Database will be created by Flask on first run
        return
    
    print(f"Found database at: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if glimpse table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='glimpse'")
        if not cursor.fetchone():
            print("Glimpse table doesn't exist yet. Will be created with correct schema.")
            conn.close()
            return
        
        # Check current schema
        cursor.execute("PRAGMA table_info(glimpse)")
        columns = cursor.fetchall()
        
        # Check if image_path is nullable
        image_path_col = [col for col in columns if col[1] == 'image_path']
        if image_path_col and image_path_col[0][3] == 0:  # notnull = 0 means nullable
            print("✓ image_path is already nullable. No migration needed.")
            conn.close()
            return
        
        print("Migrating glimpse table to make image_path optional...")
        
        # Create new table with nullable image_path
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS glimpse_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                image_path VARCHAR(300),
                video_url VARCHAR(500) NOT NULL,
                hashtags VARCHAR(500),
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Copy data from old table to new table
        cursor.execute("""
            INSERT INTO glimpse_new (id, title, description, image_path, video_url, hashtags, is_active, created_at, updated_at)
            SELECT id, title, description, image_path, video_url, hashtags, is_active, created_at, updated_at
            FROM glimpse
        """)
        
        # Drop old table
        cursor.execute("DROP TABLE glimpse")
        
        # Rename new table to original name
        cursor.execute("ALTER TABLE glimpse_new RENAME TO glimpse")
        
        conn.commit()
        print("✓ Migration completed successfully!")
        print("✓ image_path is now optional in glimpse table")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Starting Railway database migration...")
    migrate_database()
    print("Migration script completed.")
