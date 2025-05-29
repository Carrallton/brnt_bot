import os
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Инициализация
load_dotenv()
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

# Инициализация БД
def init_db():
    conn = sqlite3.connect('vpn_bot.db')
    cursor = conn.cursor()
    
    # Создаем таблицу с правильными столбцами
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        username TEXT,
        subscription_end TEXT,
        stars_balance INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# Вызываем инициализацию БД при старте
init_db()

# Утилиты для работы с БД
def get_db_connection():
    conn = sqlite3.connect('vpn_bot.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_user(user_id: int, username: str = ""):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        conn.commit()
    finally:
        conn.close()

def get_user(user_id: int):
    conn = get_db_connection()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE user_id = ?", 
            (user_id,)
        ).fetchone()
    finally:
        conn.close()

# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    add_user(message.from_user.id, message.from_user.username or "")
    
    await message.answer(
        "🔐 Добро пожаловать в VPN сервис!\n\n"
        "Используйте команды:\n"
        "/buy - Купить подписку\n"
        "/profile - Мой профиль",
        reply_markup=main_menu_kb()
    )

@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    user = get_user(message.from_user.id)
    if not user:
        return await message.answer("Сначала зарегистрируйтесь через /start")
    
    sub_status = "✅ Активна" if user["subscription_end"] and \
        datetime.strptime(user["subscription_end"], "%Y-%m-%d") > datetime.now() \
        else "❌ Не активна"
    
    await message.answer(
        f"👤 Ваш профиль:\n\n"
        f"ID: {user['user_id']}\n"
        f"Stars: {user['stars_balance']}\n"
        f"Подписка: {sub_status}\n"
        f"Действует до: {user['subscription_end'] or 'Нет подписки'}"
    )

# Клавиатуры
def main_menu_kb():
    kb = [
        [types.KeyboardButton(text="💎 Купить подписку")],
        [types.KeyboardButton(text="📊 Мой профиль")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())