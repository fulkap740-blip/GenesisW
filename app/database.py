import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    offer_id INTEGER,
    wallet TEXT,
    is_admin INTEGER DEFAULT 0,
    admin_offer_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    offer_id INTEGER,
    video_url TEXT,
    proof_url TEXT,
    views INTEGER,
    amount_auto REAL,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

def get_user(uid):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    return cursor.fetchone()

def create_user(uid):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (uid,))
    conn.commit()

def update_user_offer(uid, offer_id):
    cursor.execute("UPDATE users SET offer_id=? WHERE user_id=?", (offer_id, uid))
    conn.commit()

def update_wallet(uid, wallet):
    cursor.execute("UPDATE users SET wallet=? WHERE user_id=?", (wallet, uid))
    conn.commit()

def set_admin(uid):
    cursor.execute("UPDATE users SET is_admin=1 WHERE user_id=?", (uid,))
    conn.commit()

def set_admin_offer(uid, offer_id):
    cursor.execute("UPDATE users SET admin_offer_id=? WHERE user_id=?", (offer_id, uid))
    conn.commit()

def add_request(data):
    cursor.execute("""
    INSERT INTO requests
    (user_id, offer_id, video_url, proof_url, views, amount_auto, status)
    VALUES (?,?,?,?,?,?,?)
    """, data)
    conn.commit()