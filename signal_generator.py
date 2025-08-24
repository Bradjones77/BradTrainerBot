from data_fetcher import fetch_cmc_data

def run_signals(coins):
    """
    Returns signals for each coin:
    {
        "DOGE": {"signal": "BUY", "current_price": 0.06, "stop_loss": 0.055, "probability": 75},
        "SHIB": {"error": "No data returned"}
    }
    """
    signals = {}
    data = fetch_cmc_data(coins)
    
    for coin, coin_data in data.items():
        if "error" in coin_data:
            signals[coin] = {"error": coin_data["error"]}
            continue

        price = coin_data["current_price"]

        # Simple example: dummy signal logic
        if price < 0.1:
            signal = "BUY"
            stop_loss = price * 0.9
            probability = 70
        elif price > 100:
            signal = "SELL"
            stop_loss = price * 0.95
            probability = 80
        else:
            signal = "HOLD"
            stop_loss = price * 0.97
            probability = 60

        signals[coin] = {
            "signal": signal,
            "current_price": price,
            "stop_loss": stop_loss,
            "probability": probability
        }
    return signals
