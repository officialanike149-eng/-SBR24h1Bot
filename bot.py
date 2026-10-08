import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


WELCOME = """
👋 Welcome to Forex Guide!

Learn Forex, understand trading basics,
and improve your market knowledge step by step.

⚠️ Educational purposes only. Trading involves risk.
"""


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
            InlineKeyboardButton("🧠 Psychology", callback_data="psychology"),
            InlineKeyboardButton("❓ FAQ", callback_data="faq"),
        ],
        [
            InlineKeyboardButton("📞 Support", callback_data="support")
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME,
        reply_markup=main_menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "learn":
        text = """
📚 Forex Basics

Forex means Foreign Exchange.

It is the market where currencies are traded.

Start with:
• Currency pairs
• Buy & Sell
• Pips
• Spread
• Leverage
• Market sessions
"""

    elif query.data == "trading":
        text = """
📈 Trading Basics

A simple trading process:

1️⃣ Analyze the market
2️⃣ Find a possible setup
3️⃣ Choose Entry
4️⃣ Set Stop Loss
5️⃣ Set Take Profit
6️⃣ Manage your risk

Never risk money you cannot afford to lose.
"""

    elif query.data == "pairs":
        text = """
💱 Currency Pairs

Major examples:

EUR/USD
GBP/USD
USD/JPY
USD/CHF
AUD/USD
USD/CAD
NZD/USD

The first currency is the BASE currency.
The second is the QUOTE currency.
"""

    elif query.data == "risk":
        text = """
🛡️ Risk Management

Risk management is one of the most important
parts of trading.

• Use reasonable position sizes
• Always consider a Stop Loss
• Avoid overtrading
• Do not risk money you cannot afford to lose
• Protect your trading capital
"""

    elif query.data == "psychology":
        text = """
🧠 Trading Psychology

Good trading requires discipline.

Avoid:
❌ Revenge trading
❌ Fear-based decisions
❌ Greed
❌ Overtrading

Focus on your plan and manage your emotions.
"""

    elif query.data == "faq":
        text = """
❓ FAQ

What is Forex?
→ Trading one currency against another.

What is a pip?
→ A common unit used to measure price movement.

What is Stop Loss?
→ An order designed to limit potential loss.

What is Take Profit?
→ An order designed to close a trade at a target price.
"""

    elif query.data == "support":
        text = """
📞 Support

Need help?

Send your question here and our team
can provide general Forex education.

⚠️ We do not guarantee profits or trading results.
"""

    else:
        text = "Please choose an option from the menu."

    keyboard = [
        [InlineKeyboardButton("⬅️ Menu", callback_data="menu")]
    ]

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        WELCOME,
        reply_markup=main_menu()
    )


def main():
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN environment variable is missing. "
            "Add BOT_TOKEN in Railway Variables."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(buttons, pattern="^(?!menu$).*")
    )
    app.add_handler(
        CallbackQueryHandler(menu, pattern="^menu$")
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
