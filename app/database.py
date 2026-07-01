import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "urls.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def insert_url(short_code, original_url):
    conn = get_connection()
    conn.execute(
        "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
        (short_code, original_url),
    )
    conn.commit()
    conn.close()


def get_url(short_code):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()
    conn.close()
    return row


def code_exists(short_code):
    return get_url(short_code) is not None


def increment_clicks(short_code):
    conn = get_connection()
    conn.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,)
    )
    conn.commit()
    conn.close()
