from telegram import Bot
from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)

def send_signal(coin, signal_data):
    message = f"""🚀 {signal_data['signal']} SIGNAL: {coin}/USDT
Likelihood: {signal_data['probability']}%
Price: {signal_data['current_price']:.2f} USDT
Stop-loss: {signal_data['stop_loss']:.2f} USDT"""
    bot.send_message(chat_id='@your_telegram_channel_or_id', text=message)