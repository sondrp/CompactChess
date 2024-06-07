import sqlite3

conn = sqlite3.connect("chess.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    board TEXT NOT NULL,
    white TEXT NOT NULL,
    black TEXT NOT NULL
)
""")

conn.commit()
conn.close()