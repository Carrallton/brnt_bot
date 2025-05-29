from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional

# --- Главное меню ---
def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Купить подписку")],
            [KeyboardButton(text="📊 Мой профиль"), KeyboardButton(text="🆘 Поддержка")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

# --- Клавиатура для оплаты Stars ---
def stars_payment_kb(invoice_link: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="⭐ Оплатить 10 Stars",
            url=invoice_link  # Ссылка на инвойс Stars
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="cancel_payment"
        )
    )
    return builder.as_markup()

# --- Админ-панель ---
def admin_panel() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton(text="✉️ Рассылка", callback_data="admin_broadcast")]
        ]
    )