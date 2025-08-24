from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from data_fetcher import fetch_cmc_ohlcv, fetch_cmc_data
from analysis import compute_indicators, generate_signal
from config import TELEGRAM_TOKEN, COINS

bot = Bot(token=TELEGRAM_TOKEN)

# Define meme coins (example subset, adjust as needed)
MEME_COINS = [coin for coin in COINS if coin in ['SHIB', 'PEPE', 'DOGE', 'APE']]

# /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! I am your Crypto Signal Bot. Use /help to see commands.")

# /help command
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Show this help message\n/signalcrypto - Get current signal for main coins\n/signals - Get signals for all meme coins")

# /signalcrypto command
def signalcrypto(update: Update, context: CallbackContext):
    messages = []
    for coin in COINS:
        try:
            df = fetch_cmc_ohlcv(symbol=coin)
            df = compute_indicators(df)
            cmc_data = fetch_cmc_data(symbol=coin)
            signal_data = generate_signal(df, cmc_data)
            messages.append(f"{coin}: {signal_data['signal']} | Likelihood: {signal_data['probability']}% | Price: {signal_data['current_price']:.2f} | Stop-loss: {signal_data['stop_loss']:.2f}")
        except Exception as e:
            messages.append(f"{coin}: Error fetching signal")
    update.message.reply_text('\n'.join(messages))

# /signals command (meme coins)
def signals(update: Update, context: CallbackContext):
    messages = []
    for coin in MEME_COINS:
        try:
            df = fetch_cmc_ohlcv(symbol=coin)
            df = compute_indicators(df)
            cmc_data = fetch_cmc_data(symbol=coin)
            signal_data = generate_signal(df, cmc_data)
            messages.append(f"{coin}: {signal_data['signal']} | Likelihood: {signal_data['probability']}% | Price: {signal_data['current_price']:.2f} | Stop-loss: {signal_data['stop_loss']:.2f}")
        except Exception as e:
            messages.append(f"{coin}: Error fetching signal")
    update.message.reply_text('\n'.join(messages))

# Setup updater and handlers
updater = Updater(token=TELEGRAM_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('help', help_command))
dp.add_handler(CommandHandler('signalcrypto', signalcrypto))
dp.add_handler(CommandHandler('signals', signals))

# Start polling
updater.start_polling()
updater.idle()
