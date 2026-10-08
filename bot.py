
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

# Railway environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

WELCOME = (
    "👋 Welcome to SBR24h_Bot!\n\n"
    "Learn Forex fundamentals, currency pairs, trading concepts "
    "and risk management through simple educational lessons.\n\n"
    "📚 Choose a topic below to start learning.\n\n"
    "⚠️ Educational content only. Trading involves financial risk."
)

LESSONS = {
    "learn": (
        "📚 FOREX BASICS\n\n"
        "Forex is the market where currencies are exchanged.\n\n"
        "Learn these key terms:\n"
        "• Currency pair: two currencies quoted together\n"
        "• Pip: a common unit of price movement\n"
        "• Spread: the difference between bid and ask prices\n"
        "• Leverage: exposure larger than your deposited margin\n\n"
        "Understanding these concepts is a first step in Forex."
    ),
    "trading": (
        "📈 TRADING BASICS\n\n"
        "A trade involves buying one currency and selling another.\n\n"
        "Important concepts:\n"
        "• Buy and Sell orders\n"
        "• Entry and exit prices\n"
        "• Stop Loss and Take Profit\n"
        "• Trading plans and practice accounts\n\n"
        "Learn and practise with a demo account before risking money. "
        "No setup guarantees a profit."
    ),
    "pairs": (
        "💱 CURRENCY PAIRS\n\n"
        "Examples of major Forex pairs:\n"
        "• EUR/USD — euro and US dollar\n"
        "• GBP/USD — pound and US dollar\n"
        "• USD/JPY — US dollar and Japanese yen\n"
        "• USD/CHF — US dollar and Swiss franc\n"
        "• AUD/USD — Australian and US dollars\n\n"
        "The first currency is the base currency. "
        "The second is the quote currency."
    ),
    "risk": (
        "🛡️ RISK MANAGEMENT\n\n"
        "Protecting your capital is an important part of learning.\n\n"
        "• Understand potential losses before trading\n"
        "• Learn how position size affects risk\n"
        "• Understand Stop Loss limitations\n"
        "• Avoid borrowed money you cannot repay\n"
        "• Never assume a trade will succeed\n\n"
        "Forex trading can result in substantial losses."
    ),
    "mindset": (
        "🧠 TRADING PSYCHOLOGY\n\n"
        "Good habits can help you make more disciplined decisions.\n\n"
        "• Follow a written learning plan\n"
        "• Avoid revenge trading\n"
        "• Recognise fear and greed\n"
        "• Take breaks when emotional\n"
        "• Review decisions without chasing losses\n\n"
        "Discipline cannot remove market risk."
    ),
    "faq": (
        "❓ FREQUENTLY ASKED QUESTIONS\n\n"
        "What is Forex?\n"
        "The exchange of one currency for another.\n\n"
        "What is a demo account?\n"
        "An account for practising with simulated funds.\n\n"
        "What is a Stop Loss?\n"
        "An order intended to close a trade at a specified "
        "price to limit losses; execution is not guaranteed "
        "at that exact price.\n\n"
        "Can Forex guarantee profits?\n"
        "No. Losses are possible, and profits are never guaranteed."
    ),
    "support": (
        "💬 SUPPORT\n\n"
        "Send your question about Forex terminology or the "
        "educational lessons in this bot.\n\n"
        "This bot provides general educational information, "
        "not personalised financial advice or guaranteed trading signals."
    ),
}

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📚 Learn Forex", callback_data="learn"),
            InlineKeyboardButton("📈 Trading", callback_data="trading"),
        ],
        [
            InlineKeyboardButton("💱 Pairs", callback_data="pairs"),
            InlineKeyboardButton("🛡️ Risk", callback_data="risk"),
        ],
        [
            InlineKeyboardButton("🧠 Mindset", callback_data="mindset"),
            InlineKeyboardButton("❓ FAQ", callback_data="faq"),
        ],
        [InlineKeyboardButton("💬 Support", callback_data="support")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu")]
    ])


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.effective_message
    if message:
        await message.reply_text(
            WELCOME,
            reply_markup=main_menu(),
        )


async def show_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        WELCOME,
        reply_markup=main_menu(),
    )


async def handle_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    topic = query.data

    if topic == "menu":
        await show_menu(update, context)
        return

    text = LESSONS.get(topic)

    if text is None:
        await query.edit_message_text(
            "Please choose a topic from the main menu.",
            reply_markup=back_button(),
        )
        return

    await query.edit_message_text(
        text,
        reply_markup=back_button(),
    )


async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.effective_message
    if not message or not message.text:
        return

    question = message.text.lower()

    # Basic educational responses to common questions.
    if "what is forex" in question or question == "forex":
        answer = LESSONS["learn"]
    elif "currency pair" in question or "currency pairs" in question:
        answer = LESSONS["pairs"]
    elif "stop loss" in question:
        answer = (
            "🛡️ A Stop Loss is an order intended to close "
            "a trade when the price reaches a specified level. "
            "It may not execute at that exact price in fast markets.\n\n"
            "Learn more in the Risk section."
        )
    elif "take profit" in question:
        answer = (
            "🎯 Take Profit is an order intended to close a trade "
            "when a specified target price is reached. Execution "
            "at the exact price is not always guaranteed."
        )
    elif "pip" in question:
        answer = (
            "📘 A pip is a common unit used to measure price "
            "movement in a currency pair. Its value depends on "
            "the pair, trade size and account currency."
        )
    elif "risk" in question or "loss" in question:
        answer = LESSONS["risk"]
    elif "buy" in question or "sell" in question:
        answer = LESSONS["trading"]
    else:
        answer = (
            "📚 I can help with basic Forex education.\n\n"
            "Choose a topic below, or ask about Forex basics, "
            "currency pairs, pips, Stop Loss or Take Profit.\n\n"
            "I do not provide guaranteed signals or promise profits."
        )

    await message.reply_text(
        answer,
        reply_markup=main_menu(),
    )


def main():
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN environment variable is missing. "
            "Add BOT_TOKEN in Railway Variables."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )

    logger.info("SBR24h_Bot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
