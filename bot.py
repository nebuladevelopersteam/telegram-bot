import asyncio
import sqlite3

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ----------------- تنظیمات -----------------

TOKEN = "8747792212:AAHM7L3MYE-BiSgM96wTluBpielLjI_ki-Q"
ADMIN_ID = 8602129176

bot = Bot(TOKEN)
dp = Dispatcher()

# ----------------- دیتابیس -----------------

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT
)
""")

conn.commit()

# ----------------- منوی اصلی -----------------

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❓ سوالات متداول",
                callback_data="faq"
            )
        ],
        [
            InlineKeyboardButton(
                text="📞 پشتیبانی",
                url="https://t.me/nebula_owner_dev"
            )
        ]
    ]
)

# ----------------- منوی FAQ -----------------

faq_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 ثبت نام", callback_data="register")
        ],
        [
            InlineKeyboardButton(text="💰 قیمت", callback_data="price")
        ],
        [
            InlineKeyboardButton(text="📜 قوانین", callback_data="rules")
        ],
        [
            InlineKeyboardButton(text="🌐 درباره ما", callback_data="about")
        ],
        [
            InlineKeyboardButton(text="🔙 بازگشت", callback_data="back")
        ]
    ]
)

# ----------------- Start + ثبت کاربر -----------------

@dp.message(CommandStart())
async def start(message: Message):

    user = message.from_user

    cursor.execute("""
    INSERT OR IGNORE INTO users(user_id, username, first_name)
    VALUES(?,?,?)
    """, (user.id, user.username, user.first_name))

    conn.commit()

    await message.answer(
        "👋 سلام\nبه ربات خوش آمدید.",
        reply_markup=main_menu
    )

# ----------------- FAQ -----------------

@dp.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "❓ یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=faq_menu
    )

# ----------------- ثبت نام -----------------

@dp.callback_query(F.data == "register")
async def register(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "📝 ثبت نام\n\n"
        "برای ثبت سفارش وارد PV زیر شوید:\n\n"
        "👉 https://t.me/nebula_owner_dev",
        reply_markup=faq_menu
    )

# ----------------- قیمت -----------------

@dp.callback_query(F.data == "price")
async def price(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "💰 قیمت\n\n"
        "💎 قیمت پایه: 5,000,000 تومان\n\n"
        "برای ثبت سفارش به پشتیبانی پیام دهید.",
        reply_markup=faq_menu
    )

# ----------------- قوانین -----------------

@dp.callback_query(F.data == "rules")
async def rules(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "📜 قوانین\n\n"
        "استفاده از ربات به معنی پذیرش قوانین است.",
        reply_markup=faq_menu
    )

# ----------------- درباره ما -----------------

@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "🌐 درباره ما\n\n"
        "این ربات نسخه اولیه سیستم پشتیبانی و فروش است.",
        reply_markup=faq_menu
    )

# ----------------- بازگشت -----------------

@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.answer()

    await callback.message.edit_text(
        "👋 منوی اصلی",
        reply_markup=main_menu
    )

# ----------------- آمار کاربران -----------------

@dp.message(F.text == "/stats")
async def stats(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    await message.answer(
        f"📊 آمار ربات:\n\n👤 تعداد کاربران: {count}"
    )

# ----------------- اجرا -----------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())