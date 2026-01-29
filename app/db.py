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
            status TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            offer TEXT PRIMARY KEY,
            rate REAL
        )
        """)

        # дефолтные rate (если пусто)
        cur.execute("INSERT OR IGNORE INTO rates VALUES ('White Bird', 1.5)")
        cur.execute("INSERT OR IGNORE INTO rates VALUES ('Genesis', 2.0)")

        conn.commit()


def get_rate(offer):
    with sqlite3.connect(DB_NAME) as conn:
        row = conn.execute(
            "SELECT rate FROM rates WHERE offer = ?", (offer,)
        ).fetchone()
        return row[0]


def set_rate(offer, rate):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE rates SET rate = ? WHERE offer = ?",
            (rate, offer)
        )
        conn.commit()
