import sqlite3

conn = sqlite3.connect("chess.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
)
""")

c.execute("""INSERT INTO users (username) VALUES ("no opponent")""")

c.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    board TEXT NOT NULL,
    white TEXT NOT NULL,
    black TEXT NOT NULL,
    FOREIGN KEY (white) REFERENCES users (username),
    FOREIGN KEY (black) REFERENCES users (username)
)
""")

conn.commit()
conn.close()