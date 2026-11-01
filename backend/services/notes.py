from fastapi import APIRouter, status
import sqlite3 as db
from pathlib import Path
from pydantic import BaseModel

class Note(BaseModel):
    user_id: str
    header: str
    text: str


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR.parent / "database" / "db.db"

DB_DIR.parent.mkdir(parents=True, exist_ok=True)

def get_db(db_dir=DB_DIR):
    return db.connect(db_dir)

with get_db() as init_conn:
    init_conn.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        header TEXT NOT NULL,
        text TEXT NOT NULL
    )
    """)

@router.post("/new", status_code=status.HTTP_201_CREATED)
async def new_note(note: Note): #TODO: Refactor async db
    with get_db() as conn:
        conn.execute("""
        INSERT INTO notes (user_id, header, text) VALUES (?, ?, ?)
        """, (note.user_id, note.header, note.text))
    return {"status": "ok"}

@router.get("/all")
def get_all_notes(user_id: str):
    with get_db() as conn:
        conn.row_factory = db.Row

        notes = conn.execute(
            """
            SELECT id, header, text
            FROM notes
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchall()

    return [dict(note) for note in notes]