import sqlite3

from models.base import DB_PATH
from services.database import init_db
from services.demo_data import generate_demo_data


def test_foreign_key_integrity():
    init_db()
    generate_demo_data()
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute("PRAGMA foreign_key_check").fetchall()
        assert rows == []
    finally:
        conn.close()
