import sqlite3

db_path = r"C:\Users\YEFERSON\Desktop\Desarrollo y Proyectos\MODULO TABLAS DE RETENCION\data\trd_database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

for t in tables:
    table = t[0]
    cursor.execute(f"PRAGMA table_info({table})")
    print(f"\n{table} columns:", [c[1] for c in cursor.fetchall()])
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table} count:", cursor.fetchone()[0])
