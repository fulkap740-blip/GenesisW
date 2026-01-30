import sqlite3

DB_NAME = "database.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            wallet TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            offer TEXT,
            video_link TEXT,
            proof_link TEXT,
            views INTEGER,
            amount REAL,
            status TEXT DEFAULT 'pending',
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()


def get_rate(offer: str) -> float:
    from app.config import OFFERS
    return OFFERS[offer]["rate"]
