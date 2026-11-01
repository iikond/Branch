from fastapi import FastAPI
from .services import chat, notes
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

app.include_router(chat.router, prefix="/api/ws")
app.include_router(notes.router, prefix="/api/notes")

@app.get("/api/test")
async def test():
    return {200:"OK"}