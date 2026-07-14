from pathlib import Path
import sqlite3

base_dir = Path(__file__).resolve().parent
db_path = base_dir / "mutual_fund.db"
sql_path = base_dir / "sql" / "create_table.sql"

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
with sql_path.open("r", encoding="utf-8") as f:
    cursor.executescript(f.read())

conn.commit()
print(f"Database created successfully at: {db_path}")
conn.close()