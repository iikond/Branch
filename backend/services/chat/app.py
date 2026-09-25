# backend/services/chat/app.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random
import sqlite3
app = FastAPI()

# Простая БД SQLite
conn = sqlite3.connect("chat.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
            
# Онлайн клиенты
online = {}


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Генерируем случайный UUID для ника (как в HTML версии)
    user_id = str(random.randint(1000, 9999)) + "-" + str(random.randint(0, 999))
    online[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()

            if not data:
                break

            # Сохраняем в БД
            cur.execute("INSERT INTO messages (user_id, text) VALUES (?, ?)",
                       (user_id, data))
            conn.commit()

            # Отправляем всем подключенным (без эксклюзии для простоты)
            await broadcast(f"{user_id}: {data}")
    finally:
        online.pop(user_id, None)


async def broadcast(message: str):
    """Отправляет сообщение всем онлайн клиентам."""
    for uid, ws in list(online.items())[:10]:  # Ограничим для простоты
        try:
            await ws.send_text(message)
        except Exception as e:
            print(f"Ошибка отправки клиенту {uid}: {e}")
            pass