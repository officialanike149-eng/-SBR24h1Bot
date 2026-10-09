
import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")


# MAIN MENU: ONLY 4 OPTIONS
def main_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Learn Forex", callback_data="learn"),
            InlineKeyboardButton("💱 Currency Pairs", callback_data="pairs"),
        ],
        [
            InlineKeyboardButton("🛡️ Risk Management", callback_data="risk"),
            InlineKeyboardButton("❓ Help & FAQ", callback_data="faq"),
        ],
    ])


def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu")]
    ])


# SHORT EDUCATIONAL RESPONSES
CONTENT = {
    "learn": (
        "📚 <b>Learn Forex</b>\n\n"
        "Forex is the market where currencies are exchanged.\n\n"
        "Learn the basics:\n"
        "• Currency pairs\n"
        "• Pips and spreads\n"
        "• Buy and sell orders\n"
        "• Demo trading\n\n"
        "⚠️ Trading involves risk."
    ),

    "pairs": (
        "💱 <b>Currency Pairs</b>\n\n"
        "Examples of major Forex pairs:\n"
        "• EUR/USD — Euro / US Dollar\n"
        "• GBP/USD — Pound / US Dollar\n"
        "• USD/JPY — US Dollar / Japanese Yen\n"
        "• AUD/USD — Australian / US Dollar\n\n"
        "Currency prices can rise or fall."
    ),

    "risk": (
        "🛡️ <b>Risk Management</b>\n\n"
        "• Learn position sizing.\n"
        "• Understand stop-loss orders.\n"
        "• Be careful with leverage.\n"
        "• Never risk money needed for essentials.\n"
        "• Practise with a demo account.\n\n"
        "⚠️ You can lose money trading Forex."
    ),

    "faq": (
        "❓ <b>Help & FAQ</b>\n\n"
        "<b>Is Forex risk-free?</b>\n"
        "No. Losses are possible.\n\n"
        "<b>Can beginners learn?</b>\n"
        "Yes. Start with basic lessons and demo practice.\n\n"
        "<b>Does this bot give trading signals?</b>\n"
        "No. It provides educational information only."
    ),
}


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "👋 <b>Welcome to Forex Guide!</b>\n\n"
        "Learn Forex basics with simple lessons.\n"
        "Choose an option below to get started.\n\n"
        "⚠️ Education only. Trading involves risk.",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


# MENU
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "📋 <b>Forex Guide Menu</b>\nChoose an option:",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


# BUTTONS
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        await query.edit_message_text(
            "📋 <b>Forex Guide Menu</b>\nChoose an option:",
            reply_markup=main_menu(),
            parse_mode="HTML",
        )
        return

    if query.data in CONTENT:
        await query.edit_message_text(
            CONTENT[query.data],
            reply_markup=back_menu(),
            parse_mode="HTML",
        )
        return

    await query.edit_message_text(
        "Please choose an option from the menu.",
        reply_markup=main_menu(),
    )


# SIMPLE TEXT REPLIES
async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.effective_message
    if not message or not message.text:
        return

    text = message.text.lower().strip()

    if text in ("hi", "hello", "hey"):
        reply = "👋 Hello! Choose a Forex topic below."
    elif "pair" in text or "eur/usd" in text or "gbp/usd" in text:
        reply = CONTENT["pairs"]
    elif "risk" in text or "stop loss" in text:
        reply = CONTENT["risk"]
    elif "help" in text or "faq" in text:
        reply = CONTENT["faq"]
    elif "forex" in text or "trading" in text:
        reply = CONTENT["learn"]
    else:
        reply = (
            "Thanks for your message!\n\n"
            "Please choose a menu option to explore Forex basics."
        )

    await message.reply_text(
        reply,
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


# ERROR LOGGING
async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.error("Bot error: %s", context.error)


# START BOT
def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Add it in Railway Variables."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler)
    )
    app.add_error_handler(error_handler)

    logger.info("Forex Guide bot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
