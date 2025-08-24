# data_fetcher.py

import requests
from config import CMC_API_KEY

CMC_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

def fetch_cmc_data(coins):
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
    }

    coin_list = ",".join(coins)
    params = {"symbol": coin_list, "convert": "USD"}

    response = requests.get(CMC_API_URL, headers=headers, params=params)
    data = response.json()

    result = {}
    for coin in coins:
        if coin in data.get("data", {}):
            price = data["data"][coin]["quote"]["USD"]["price"]
            result[coin] = {"current_price": price}
        else:
            result[coin] = {"error": "No data returned"}

    return result
