from data_fetcher import fetch_cmc_ohlcv, fetch_cmc_data
from analysis import compute_indicators, generate_signal
from telegram_bot import send_signal
from config import COINS

def run_signals():
    for coin in COINS:
        try:
            df = fetch_cmc_ohlcv(symbol=coin)
            df = compute_indicators(df)
            cmc_data = fetch_cmc_data(symbol=coin)
            signal_data = generate_signal(df, cmc_data)
            send_signal(coin, signal_data)
        except Exception as e:
            print(f'Error processing {coin}:', e)