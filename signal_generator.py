from data_fetcher import fetch_cmc_ohlcv, fetch_cmc_data
from analysis import compute_indicators, generate_signal
import time

def run_signals(coins):
    """
    Generate signals for a list of coins and return as a dictionary.
    """
    signals = {}
    for coin in coins:
        try:
            # Fetch market data
            df = fetch_cmc_ohlcv(symbol=coin)
            df = compute_indicators(df)
            cmc_data = fetch_cmc_data(symbol=coin)

            # Generate signal
            signal_data = generate_signal(df, cmc_data)

            signals[coin] = {
                "signal": signal_data["signal"],
                "current_price": signal_data["current_price"],
                "stop_loss": signal_data["stop_loss"],
                "probability": signal_data["probability"]
            }

        except Exception as e:
            signals[coin] = {"error": str(e)}

        time.sleep(1)  # Avoid API rate limits

    return signals
