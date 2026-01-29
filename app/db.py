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
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            rate REAL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            offer_id INTEGER,
            video TEXT,
            proof TEXT,
            views INTEGER,
            amount REAL,
            status TEXT
        )
        """)

        cur.execute("SELECT COUNT(*) FROM offers")
        if cur.fetchone()[0] == 0:
            cur.executemany(
                "INSERT INTO offers (id, name, rate) VALUES (?,?,?)",
                [
                    (1, "White Bird", 1.5),
                    (2, "Genesis", 2.0),
                ]
            )
        conn.commit()

def get_rate(offer_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT rate FROM offers WHERE id=?", (offer_id,))
        return cur.fetchone()[0]

def set_rate(offer_id: int, rate: float):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE offers SET rate=? WHERE id=?",
            (rate, offer_id)
        )
        conn.commit()