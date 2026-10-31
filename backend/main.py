from fastapi import FastAPI
from .services import chat, pages
from pathlib import Path
import sqlite3 as db

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database" / "db.db"

def get_db(db_dir = DB_DIR):
    return db.connect(db_dir)

with get_db() as init_conn:
    init_conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        nickname TEXT NOT NULL,
        hashed_password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

app = FastAPI()

app.include_router(chat.router, prefix="/ws")
app.include_router(pages.router)