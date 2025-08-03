import asyncio
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
import config

router = Router()

# Главное меню
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪙 О монете", callback_data="about")],
        [InlineKeyboardButton(text="💰 Как купить", callback_data="how_to_buy")],
        [InlineKeyboardButton(text="🌐 Ссылки", callback_data="links")]
    ])

# Назад
def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])

# Ссылки
def links_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Сайт", url="https://vurn.io")],
        [InlineKeyboardButton(text="📢 Twitter", url="https://x.com/dmitrij15142")],
        [InlineKeyboardButton(text="💬 Telegram", url="https://t.me/VURNINFO_bot")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])

# /start
@router.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в <b>VURN Bot</b>!\n\n"
        "🪙 <b>VURN</b> — децентрализованный токен в сети TON.\n\n"
        "📌 Используй кнопки ниже, чтобы узнать больше:",
        reply_markup=main_menu(),
        parse_mode=ParseMode.HTML
    )

# О монете
@router.callback_query(F.data == "about")
async def callback_about(call: CallbackQuery):
    await call.message.edit_text(
        "🪙 <b>О токене VURN</b>\n\n"
        "VURN — децентрализованный токен в сети TON.\n"
        "Контракт: <code>[вставь_контракт]</code>",
        reply_markup=back_button(),
        parse_mode=ParseMode.HTML
    )

# Как купить (с изображением)
@router.callback_query(F.data == "how_to_buy")
async def callback_how_to_buy(call: CallbackQuery):
    await call.message.answer(
        "💰 <b>Как купить VURN:</b>\n\n"
        "1. Установи криптокошелёк с поддержкой сети TON (например, <a href='https://tonkeeper.com/'>Tonkeeper</a>)\n"
        "2. Пополни кошелёк монетами TON\n"
        "3. Перейди на DEX, например <a href='https://dedust.io/pools/EQBvLARWhyH1cihbus3WyBbSvXbx0N6SLVlQ4aNKjNE9SqjL'>DeDust.io</a>",
        parse_mode=ParseMode.HTML
    )

    try:
        screenshot = FSInputFile("Screenshot_1.png")
        await call.message.answer_photo(
            screenshot,
            caption="⬆️ Нажми кнопку <b>Swap</b>",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await call.message.answer(f"❌ Ошибка при загрузке фото: {e}")

    await call.message.answer(
        "4. Найди токен VURN по контракту и обменяй",
        parse_mode=ParseMode.HTML,
        reply_markup=back_button()
    )

# Ссылки
@router.callback_query(F.data == "links")
async def callback_links(call: CallbackQuery):
    await call.message.edit_text(
        "🌐 <b>Полезные ссылки:</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=links_menu()
    )

# Назад
@router.callback_query(F.data == "back")
async def callback_back(call: CallbackQuery):
    await call.message.edit_text(
        "👋 Добро пожаловать в <b>VURN Bot</b>!\n\n"
        "🪙 <b>VURN</b> — децентрализованный токен в сети TON.\n\n"
        "📌 Используй кнопки ниже, чтобы узнать больше:",
        reply_markup=main_menu(),
        parse_mode=ParseMode.HTML
    )

# Запуск
async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
