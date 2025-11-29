"""
Legacy initializer for the pre-star-schema warehouse (model/schema.sql).
Prefer `etl/load.py`, which builds the current star schema in
`warehouse/pierrot_bi.db`. This script is kept for historical reference and
tests against the archived schema.
"""
import sqlite3
from pathlib import Path

def init_database():
    """Create all tables from schema.sql in the SQLite database."""
    # Paths
    db_path = Path(__file__).parent.parent / "studio_pierrot.db"
    schema_path = Path(__file__).parent.parent / "model" / "schema.sql"
    
    # Read schema
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    # Connect and execute
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_sql)
        conn.commit()
        print(f"✓ Database initialized successfully at {db_path}")
        
        # Verify tables were created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        print(f"✓ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    init_database()
