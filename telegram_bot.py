from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, COINS
from signal_generator import run_signals
import asyncio

# Emoji mapping for signals
SIGNAL_DISPLAY = {
    "BUY": "🚀🟢⬆️ **BUY** 🚀",
    "SELL": "💥🔴⬇️ **SELL** 💥",
    "HOLD": "⏸️🟡⚖️ **HOLD** ⏸️"
}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! I am your Crypto Signal Bot. Use /help to see commands."
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/signalcrypto - Get current signal for main coins\n"
        "/signals - Get signals for all meme coins"
    )

# /signalcrypto command
async def signalcrypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signals = run_signals(COINS)
    messages = []
    for coin, data in signals.items():
        if "error" in data:
            messages.append(f"{coin}: ❌ Error fetching signal ({data['error']})")
        else:
            signal_text = SIGNAL_DISPLAY.get(data["signal"], "❔ UNKNOWN")
            messages.append(
                f"💎 {coin} 💎\n"
                f"Signal: {signal_text}\n"
                f"Price: 💰 {data['current_price']:.2f} USDT\n"
                f"Stop-loss: 🛑 {data['stop_loss']:.2f} USDT\n"
                f"Likelihood: 📊 {data['probability']}%\n"
                "────────────────────────"
            )
    await update.message.reply_text("\n".join(messages))

# /signals command for meme coins
MEME_COINS = ['DOGE', 'SHIB', 'APE', 'PEPE']

async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signals = run_signals(MEME_COINS)
    messages = []
    for coin, data in signals.items():
        if "error" in data:
            messages.append(f"{coin}: ❌ Error fetching signal ({data['error']})")
        else:
            signal_text = SIGNAL_DISPLAY.get(data["signal"], "❔ UNKNOWN")
            messages.append(
                f"💎 {coin} 💎\n"
                f"Signal: {signal_text}\n"
                f"Price: 💰 {data['current_price']:.2f} USDT\n"
                f"Stop-loss: 🛑 {data['stop_loss']:.2f} USDT\n"
                f"Likelihood: 📊 {data['probability']}%\n"
                "────────────────────────"
            )
    await update.message.reply_text("\n".join(messages))

# Build application
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("signalcrypto", signalcrypto))
app.add_handler(CommandHandler("signals", signals))

# Async function to start bot safely
async def main():
    await app.bot.delete_webhook()  # Remove webhook to avoid conflicts
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
