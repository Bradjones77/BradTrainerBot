import requests
from config import CMC_API_KEY

CMC_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": CMC_API_KEY,
}

def fetch_cmc_data(coins):
    """
    Fetch current price data from CoinMarketCap for a list of coins.
    Returns a dictionary like:
    {
        "DOGE": {"price": 0.06, "symbol": "DOGE"},
        "SHIB": {"price": 0.00001, "symbol": "SHIB"},
    }
    """
    coin_list = ",".join(coins)
    try:
        response = requests.get(CMC_API_URL, headers=headers, params={"symbol": coin_list, "convert": "USD"})
        response.raise_for_status()
        data = response.json()
        result = {}
        for coin in coins:
            if coin in data.get("data", {}):
                price = data["data"][coin]["quote"]["USD"]["price"]
                result[coin] = {
                    "current_price": price
                }
            else:
                result[coin] = {"error": "No data returned"}
        return result
    except Exception as e:
        # Return error for all coins if request fails
        return {coin: {"error": str(e)} for coin in coins}
