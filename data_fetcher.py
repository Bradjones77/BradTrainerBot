import pandas as pd
import requests
from config import CMC_API_KEY

def fetch_cmc_ohlcv(symbol="BTC"):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"symbol": symbol}
    response = requests.get(url, headers=headers, params=params).json()
    data = response['data'][symbol]
    df = pd.DataFrame([{
        'timestamp': pd.Timestamp.now(),
        'open': data['quote']['USD']['price'],
        'high': data['quote']['USD']['price'],
        'low': data['quote']['USD']['price'],
        'close': data['quote']['USD']['price'],
        'volume': data['quote']['USD']['volume_24h']
    }])
    return df

def fetch_cmc_data(symbol="BTC"):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"symbol": symbol}
    response = requests.get(url, headers=headers, params=params).json()
    data = response['data'][symbol]
    return {
        'price': data['quote']['USD']['price'],
        'market_cap': data['quote']['USD']['market_cap'],
        'volume_24h': data['quote']['USD']['volume_24h']
    }