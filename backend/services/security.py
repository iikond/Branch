import sqlite3
from pwdlib import PasswordHash

# Инициализируем хэшер паролей (по умолчанию использует bcrypt)
password_hash = PasswordHash.recommended()

# -------------------------------------------------------------
# 1. РЕГИСТРАЦИЯ: Хешируем пароль перед записью в SQLite
# -------------------------------------------------------------
def register_user(username: str, raw_password: str):
    # Превращаем "my_secret_123" в строку вида "$bcrypt$v=2$..."
    hashed_password = password_hash.hash(raw_password)

    with sqlite3.connect("database.db") as conn:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_password)
        )

# -------------------------------------------------------------
# 2. АУТЕНТИФИКАЦИЯ: Проверяем введённый пароль при входе
# -------------------------------------------------------------
def verify_user(username: str, raw_password: str) -> bool:
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()

    if not row:
        return False  # Пользователь не найден

    stored_hash = row[0]
    
    # Сравниваем введённый пароль с хешем из БД
    return password_hash.verify(raw_password, stored_hash)