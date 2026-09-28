from fastapi import FastAPI, WebSocket, APIRouter
import random
import sqlite3 as db
import time
from pathlib import Path
from datetime import datetime

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR.parent / "database" / "db.db"

DB_DIR.parent.mkdir(parents=True, exist_ok=True)


def get_db(db_dir=DB_DIR):
    return db.connect(db_dir)


with get_db() as init_conn:
    init_conn.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        reciver_id INTEGER,
        text TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

# Онлайн клиенты
online = {}


async def broadcast(message: str):
    """Отправляет сообщение всем онлайн клиентам."""
    for uid, ws in list(online.items()):
        try:
            await ws.send_text(message)
        except Exception as e:
            print(f"Ошибка отправки клиенту {uid}: {e}")
            pass


@router.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Генерируем случайный UUID для ника (как в HTML версии)
    sender_id = str(random.randint(1000, 9999)) + "-" + str(random.randint(0, 999))
    online[sender_id] = websocket

    try:
        # 1. Оповещаем остальных, что вошел новый юзер
        await broadcast(f"Подключено (ID: {sender_id})")

        # 2. Шлем историю ТОЛЬКО новому клиенту (не через broadcast!)
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT sender_id, text FROM messages ORDER BY created_at ASC")
            for msg_sender_id, msg_text in cur.fetchall():
                await websocket.send_text(f"{msg_sender_id}: {msg_text}")

        # Теперь ждём входящих сообщений
        while True:
            data = await websocket.receive_text()

            if not data:
                break

            with get_db() as conn:
                conn.execute(
                    "INSERT INTO messages (sender_id, text) VALUES (?, ?)", (sender_id, data)
                )

            # Отправляем всем подключенным
            await broadcast(f"{sender_id}: {data}")
    finally:
        online.pop(sender_id, None)
