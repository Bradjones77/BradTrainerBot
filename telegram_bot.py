# telegram_bot.py

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, COINS, MEME_COINS
from signal_generator import run_signals

SIGNAL_DISPLAY = {
    "BUY": "🚀🟢⬆️ **BUY** 🚀",
    "SELL": "💥🔴⬇️ **SELL** 💥",
    "HOLD": "⏸️🟡⚖️ **HOLD** ⏸️"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! I am your Crypto Signal Bot. Use /help to see commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/signalcrypto - Get current signal for main coins\n"
        "/signals - Get signals for all meme coins"
    )

async def signalcrypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signals = run_signals(COINS)
    messages = []
    for idx, (coin, data) in enumerate(signals.items(), start=1):
        if "error" in data:
            messages.append(f"{coin}: ❌ Error fetching signal ({data['error']})")
        else:
            signal_text = SIGNAL_DISPLAY.get(data["signal"], "❔ UNKNOWN")
            messages.append(
                f"💎 {coin} 💎\n"
                f"Signal: {signal_text}\n"
                f"Price: 💰 {data['current_price']:.4f} USDT\n"
                f"Stop-loss: 🛑 {data['stop_loss']:.4f} USDT\n"
                f"Likelihood: 📊 {data['probability']}%\n"
                "────────────────────────"
            )
        if idx % 5 == 0 or idx == len(signals):
            await update.message.reply_text("\n".join(messages))
            messages = []
            await asyncio.sleep(1)

async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signals_data = run_signals(MEME_COINS)
    messages = []
    for idx, (coin, data) in enumerate(signals_data.items(), start=1):
        if "error" in data:
            messages.append(f"{coin}: ❌ Error fetching signal ({data['error']})")
        else:
            signal_text = SIGNAL_DISPLAY.get(data["signal"], "❔ UNKNOWN")
            messages.append(
                f"💎 {coin} 💎\n"
                f"Signal: {signal_text}\n"
                f"Price: 💰 {data['current_price']:.4f} USDT\n"
                f"Stop-loss: 🛑 {data['stop_loss']:.4f} USDT\n"
                f"Likelihood: 📊 {data['probability']}%\n"
                "────────────────────────"
            )
        if idx % 5 == 0 or idx == len(signals_data):
            await update.message.reply_text("\n".join(messages))
            messages = []
            await asyncio.sleep(1)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("signalcrypto", signalcrypto))
app.add_handler(CommandHandler("signals", signals))

async def main():
    await app.bot.delete_webhook()
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
