import sqlite3
from pathlib import Path

db_path = Path("studio_pierrot.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print(f"Database: {db_path}")
print(f"Tables found: {len(tables)}\n")

for table_name in [t[0] for t in tables]:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  {table_name:30} | {count:>6} records")

conn.close()
