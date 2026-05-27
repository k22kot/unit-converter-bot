"""
bot.py — Telegram-бот с Mini App через Menu Button.

Переменные окружения:
  TELEGRAM_BOT_TOKEN  — токен от @BotFather
  MINI_APP_URL        — публичный URL вашего index.html
                        (например: https://yoursite.com/index.html
                         или https://your-project.vercel.app)
"""

import logging
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from converter import convert_message, is_bare_number

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MINI_APP_URL = os.environ.get("MINI_APP_URL", "")

# ─── Клавиатуры ───────────────────────────────────────────────────────────────

def main_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton("📏 Расстояние",  callback_data="cat:distance"),
            InlineKeyboardButton("⚖️ Вес",         callback_data="cat:weight"),
        ],
        [
            InlineKeyboardButton("🌡 Температура", callback_data="cat:temperature"),
            InlineKeyboardButton("🧴 Объём",       callback_data="cat:volume"),
        ],
    ]
    # Кнопка открытия Mini App — показываем только если URL задан
    if MINI_APP_URL:
        rows.append([
            InlineKeyboardButton(
                "🚀 Открыть приложение",
                web_app=WebAppInfo(url=MINI_APP_URL),
            )
        ])
    rows.append([InlineKeyboardButton("❓ Помощь", callback_data="help")])
    return InlineKeyboardMarkup(rows)


BACK_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("◀️ Назад", callback_data="back")]
])

CATEGORY_HINTS = {
    "distance": (
        "📏 *Расстояние*\n\n"
        "Примеры:\n"
        "• `100 km` или `100 километров`\n"
        "• `5 miles` или `5 миль`\n"
        "• `6 feet` или `6 футов`\n"
        "• `10 инч` или `10 дюймов`\n\n"
        "Понимаю сокращения и опечатки 😉"
    ),
    "weight": (
        "⚖️ *Вес*\n\n"
        "Примеры:\n"
        "• `70 kg` или `70 кило`\n"
        "• `150 lbs` или `150 фунтов`\n"
        "• `500 грамм` или `17 oz`\n\n"
        "Понимаю сокращения и опечатки 😉"
    ),
    "temperature": (
        "🌡 *Температура*\n\n"
        "Примеры:\n"
        "• `98.6 F` или `36.6 C`\n"
        "• `212 фаренгейт` или `100 цельсий`\n"
        "• `32 форингейт` — тоже пойдёт 😄\n\n"
        "Понимаю сокращения и опечатки 😉"
    ),
    "volume": (
        "🧴 *Объём*\n\n"
        "Примеры:\n"
        "• `2 литра` или `2 liters`\n"
        "• `1 gallon` или `1 галлон`\n"
        "• `500 мл` или `16 fl oz`\n\n"
        "Понимаю сокращения и опечатки 😉"
    ),
}

HELP_TEXT = (
    "🤖 *Конвертер единиц США ↔ РФ*\n\n"
    "Я умею переводить:\n"
    "• 📏 Расстояние — км, мили, футы, дюймы\n"
    "• ⚖️ Вес — кг, фунты, граммы, унции\n"
    "• 🌡 Температура — °C, °F, K\n"
    "• 🧴 Объём — литры, галлоны, пинты, fl oz\n\n"
    "Пиши на *русском или английском*, с сокращениями или опечатками — разберусь.\n\n"
    "Или открой приложение кнопкой в меню 👇"
)


def unit_keyboard(pending_value: str) -> InlineKeyboardMarkup:
    v = pending_value
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("км",     callback_data=f"unit:{v}:km"),
            InlineKeyboardButton("миля",   callback_data=f"unit:{v}:mi"),
            InlineKeyboardButton("м",      callback_data=f"unit:{v}:m"),
            InlineKeyboardButton("фут",    callback_data=f"unit:{v}:ft"),
        ],
        [
            InlineKeyboardButton("кг",     callback_data=f"unit:{v}:kg"),
            InlineKeyboardButton("фунт",   callback_data=f"unit:{v}:lb"),
            InlineKeyboardButton("г",      callback_data=f"unit:{v}:g"),
            InlineKeyboardButton("унция",  callback_data=f"unit:{v}:oz"),
        ],
        [
            InlineKeyboardButton("°C",     callback_data=f"unit:{v}:C"),
            InlineKeyboardButton("°F",     callback_data=f"unit:{v}:F"),
            InlineKeyboardButton("литр",   callback_data=f"unit:{v}:l"),
            InlineKeyboardButton("галлон", callback_data=f"unit:{v}:gal"),
        ],
    ])


# ─── Хэндлеры ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n{HELP_TEXT}",
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )


async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /app — открывает Mini App."""
    if not MINI_APP_URL:
        await update.message.reply_text(
            "Mini App не настроен. Задай переменную MINI_APP_URL.",
            reply_markup=main_keyboard(),
        )
        return
    await update.message.reply_text(
        "Открываю конвертер 👇",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🚀 Открыть", web_app=WebAppInfo(url=MINI_APP_URL))
        ]]),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("cat:"):
        category = data.split(":")[1]
        context.user_data["category"] = category
        await query.edit_message_text(
            CATEGORY_HINTS[category],
            parse_mode="Markdown",
            reply_markup=BACK_KEYBOARD,
        )

    elif data.startswith("unit:"):
        _, raw_value, unit_code = data.split(":", 2)
        result = convert_message(f"{raw_value} {unit_code}")
        if result:
            await query.edit_message_text(
                result, parse_mode="Markdown", reply_markup=main_keyboard()
            )
        else:
            await query.edit_message_text("Что-то пошло не так 🤔", reply_markup=main_keyboard())

    elif data == "help":
        await query.edit_message_text(
            HELP_TEXT, parse_mode="Markdown", reply_markup=main_keyboard()
        )

    elif data == "back":
        context.user_data.pop("category", None)
        await query.edit_message_text("Выбери раздел 👇", reply_markup=main_keyboard())


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    category_hint = context.user_data.get("category")

    if is_bare_number(text):
        safe = text.replace(" ", "").replace(",", ".")
        await update.message.reply_text(
            f"Число *{text}* — в каких единицах? 👇",
            parse_mode="Markdown",
            reply_markup=unit_keyboard(safe),
        )
        return

    result = convert_message(text, category_hint=category_hint)
    if result:
        await update.message.reply_text(result, parse_mode="Markdown", reply_markup=main_keyboard())
    else:
        await update.message.reply_text(
            "🤔 Не смог распознать единицу.\n"
            "Попробуй: `100 км`, `212 F`, `2 галлона`",
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )


# ─── Установка Menu Button при старте ────────────────────────────────────────

async def post_init(app: Application) -> None:
    """Устанавливает кнопку меню как только бот запустился."""
    if MINI_APP_URL:
        await app.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="⇄ Конвертер",
                web_app=WebAppInfo(url=MINI_APP_URL),
            )
        )
        logger.info(f"Menu Button установлена → {MINI_APP_URL}")
    else:
        logger.warning(
            "MINI_APP_URL не задан — Menu Button не установлена. "
            "Задай переменную окружения и перезапусти бота."
        )


# ─── Запуск ───────────────────────────────────────────────────────────────────

def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Задай переменную окружения TELEGRAM_BOT_TOKEN")

    app = (
        Application.builder()
        .token(token)
        .post_init(post_init)   # ← устанавливаем Menu Button при старте
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  start))
    app.add_handler(CommandHandler("app",   app_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    logger.info("Бот запущен. Ctrl+C для остановки.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
