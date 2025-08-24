import asyncio
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, COINS  # COINS = main coins
from signal_generator import run_signals

# Emoji mapping for signals
SIGNAL_DISPLAY = {
    "BUY": "🚀🟢⬆️ **BUY** 🚀",
    "SELL": "💥🔴⬇️ **SELL** 💥",
    "HOLD": "⏸️🟡⚖️ **HOLD** ⏸️"
}

# List of all meme coins
MEME_COINS = [
    'BTC','ETH','USDT','BNB','XRP','ADA','DOGE','MATIC','SOL','DOT','SHIB','LTC','TRX','AVAX',
    'UNI','CRO','NEAR','FTM','ATOM','ALGO','LINK','XLM','BCH','VET','ICP','FIL','EGLD','APE',
    'EOS','THETA','HBAR','SAND','GRT','CHZ','KSM','STX','QNT','CFX','ZIL','ENJ','BAT','DCR',
    'NEO','1INCH','FLOW','LRC','ZRX','RUNE','CELO','AR','KAVA','MANA','UMA','REV','KNC','HNT',
    'OKB','CRV','MINA','AUDIO','OCEAN','LPT','ANKR','GLM','CVX','BAL','SRM','IOST','SKL','SXP',
    'XTZ','IOTA','XEM','QTUM','FTT','WAXP','MKR','DGB','HIVE','OGN','STORJ','LUNA','RSR','AMP',
    'XCH','SC','NANO','GNO','ZEN','ARDR','OXT','REQ','REN','ICX','COTI','NKN','DENT','STMX','FRONT',
    'AKRO','LSK','CKB','PUNDIX','CVC','ONT','LOOM','FET','POLY','TWT','RAY','MASK','API3','FXS',
    'SPELL','MTL','KEEP','DODO','PERP','SUSHI','BTRST','KP3R','TRIBE','RLC','WOO','XVS','CAKE',
    'ALPHA','TORN','AAVE','COMP','SNX','YFI','BAL','CRV','REN','ZRX','CEL','BAND','STORJ','ANT',
    'MANA','CHZ','OGN','GRT','BAT','KNC','DGB','HBAR','LRC','ENJ','NEO','IOST','FTT','KAVA','RUNE',
    'CELO','HNT','OKB','MKR','LPT','AUDIO','OCEAN','GLM','CVX','ANKR','AR','THETA','SAND','FTM',
    'ALGO','ATOM','AVAX','TRX','LTC','SOL','MATIC','DOGE','ADA','XRP','BNB','ETH','BTC'
]

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

# /signalcrypto command for main coins
async def signalcrypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signals = run_signals(COINS)  # pass main coin list
    messages = []
    for idx, (coin, data) in enumerate(signals.items(), start=1):
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
        # Send batch every 10 coins
        if idx % 10 == 0 or idx == len(signals):
            await update.message.reply_text("\n".join(messages))
            messages = []
            await asyncio.sleep(1)

# /signals command for all meme coins
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
                f"Price: 💰 {data['current_price']:.2f} USDT\n"
                f"Stop-loss: 🛑 {data['stop_loss']:.2f} USDT\n"
                f"Likelihood: 📊 {data['probability']}%\n"
                "────────────────────────"
            )
        # Send batch every 10 coins
        if idx % 10 == 0 or idx == len(signals_data):
            await update.message.reply_text("\n".join(messages))
            messages = []
            await asyncio.sleep(1)

# Build the bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("signalcrypto", signalcrypto))
app.add_handler(CommandHandler("signals", signals))

# Start bot safely
async def main():
    await app.bot.delete_webhook()  # remove webhook conflicts
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
