"""
Verify the database schema and display table information.
"""
import sqlite3
from pathlib import Path

def verify_database():
    """Display all tables and their structure."""
    db_path = Path(__file__).parent.parent / "studio_pierrot.db"

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()

        print(f"Found {len(tables)} tables in studio_pierrot.db:\n")

        for (table_name,) in tables:
            print(f"  {table_name}")
            # table_name comes from sqlite_master query, safe for PRAGMA
            cursor.execute(f"PRAGMA table_info({table_name});")  # nosec
            columns = cursor.fetchall()
            for col in columns:
                col_id, name, type_, notnull, default, pk = col
                pk_marker = " [PK]" if pk else ""
                print(f"   - {name}: {type_}{pk_marker}")
            print()

        print("Database schema verification complete!")

if __name__ == "__main__":
    verify_database()
