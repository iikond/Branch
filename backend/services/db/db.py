import sqlite3

def connect(name: str) -> sqlite3.Connection:
    return sqlite3.connect(name)

def create_table(conn: sqlite3.Connection, table_name: str, columns: list[str]):
    cursor = conn.cursor()
    # Объединяем список колонок в одну строку через запятую
    cols_str = ", ".join(columns)
    # Используем f-строку (обязательна буква f перед кавычками)
    # Имена таблиц/колонок оборачиваем в двойные кавычки для защиты от служебных слов SQLite
    query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({cols_str})'
    
    cursor.execute(query)
    conn.commit()

def insert_data(conn: sqlite3.Connection, table_name: str, data: dict):
    cursor = conn.cursor()
    # Экранируем имена колонок
    keys = ', '.join([f'"{k}"' for k in data.keys()])
    placeholders = ', '.join(['?'] * len(data))
    
    query = f'INSERT INTO "{table_name}" ({keys}) VALUES ({placeholders})'
    
    # Передаем значения как безопасные параметры
    cursor.execute(query, list(data.values()))
    conn.commit()