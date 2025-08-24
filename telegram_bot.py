from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from data_fetcher import fetch_cmc_ohlcv, fetch_cmc_data
from analysis import compute_indicators, generate_signal
from config import TELEGRAM_TOKEN, COINS
import time

# Meme coins with verified CoinMarketCap symbols
MEME_COINS = ['DOGE', 'SHIB', 'APE', 'PEPE']

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! I am your Crypto Signal Bot. Use /help to see commands.")

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
    messages = []
    for coin in COINS:
        try:
            df = fetch_cmc_ohlcv(symbol=coin)
            df = compute_indicators(df)
            cmc_data = fetch_cmc_data(symbol=coin)
            signal_data = generate_signal(df, cmc_data)
            messages.append(f"{coin}: {signal_data['signal']} | Likelihood: {signal_data['probability']}% | Price: {signal_data['current_price']:.2f} | Stop-loss: {signal_data['stop_loss']:.2f}")
        except Exception as e:
            messages.append(f"{coin}: Error fetching signal ({e})")
        time.sleep(1)  # delay to avoid hitting API rate limits
    await update.message.reply_text('\n'.join(messages))

# /signals command for meme coins
async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages = []
    for coin in MEME_COINS:
        try:
            df = fetch_cmc_ohlcv(symbol=coin)
            df = compute_indicators(df)
            cmc_data = fetch_cmc_data(symbol=coin)
            signal_data = generate_signal(df, cmc_data)
            messages.append(f"{coin}: {signal_data['signal']} | Likelihood: {signal_data['probability']}% | Price: {signal_data['current_price']:.2f} | Stop-loss: {signal_data['stop_loss']:.2f}")
        except Exception as e:
            messages.append(f"{coin}: Error fetching signal ({e})")
        time.sleep(1)  # delay to avoid hitting API rate limits
    await update.message.reply_text('\n'.join(messages))

# Build application
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("signalcrypto", signalcrypto))
app.add_handler(CommandHandler("signals", signals))

# Run bot
app.run_polling()
