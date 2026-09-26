from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random
import sqlite3
import time
from datetime import datetime

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
        # 🟢 ОТПРАВЛЯЕМ ВСЕ ИСТОРИЧЕСКИЕ СООБЩЕНИЯ ПРИБЫТИЮ!
        await broadcast(f"🟢 Подключено (ID: {user_id})")
        
        # Загружаем всю историю сообщений из БД
        cur.execute("SELECT user_id, text, created_at FROM messages ORDER BY created_at ASC")
        historical_messages = cur.fetchall()
        
        for msg_user_id, msg_text, msg_created_at in historical_messages:
            await broadcast(f"{msg_user_id}: {msg_text}")
        
        # Теперь ждём входящих сообщений
        while True:
            data = await websocket.receive_text()

            if not data:
                break

            # Сохраняем в БД
            cur.execute("INSERT INTO messages (user_id, text) VALUES (?, ?)",
                       (user_id, data))
            conn.commit()

            # Отправляем всем подключенным
            await broadcast(f"{user_id}: {data}")
    finally:
        online.pop(user_id, None)


async def broadcast(message: str):
    """Отправляет сообщение всем онлайн клиентам."""
    for uid, ws in list(online.items()):  # Убрал [:10] для полных обновлений
        try:
            await ws.send_text(message)
        except Exception as e:
            print(f"Ошибка отправки клиенту {uid}: {e}")
            pass