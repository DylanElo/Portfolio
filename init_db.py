import sqlite3
from pathlib import Path

def init_db():
    db_path = Path("studio_pierrot.db")
    schema_path = Path("projects/studio-pierrot-bi/model/schema.sql")
    
    print(f"Initializing DB at {db_path} using {schema_path}")
    
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        
    conn.executescript(schema_sql)
    conn.close()
    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    init_db()
