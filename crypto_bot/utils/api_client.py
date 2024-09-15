import requests
from config.settings import API_KEY, API_SECRET, EXCHANGE_URL

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': API_KEY,
        })

    def get_price_data(self, symbol="BTCUSDT"):
        url = f"{EXCHANGE_URL}/api/v3/klines"
        params = {
            'symbol': symbol,
            'interval': '1m',
            'limit': 500
        }
        response = self.session.get(url, params=params)
        return [float(kline[4]) for kline in response.json()]

    def set_leverage(self, leverage, symbol="BTCUSDT"):
        url = f"{EXCHANGE_URL}/api/v3/leverage"
        params = {
            'symbol': symbol,
            'leverage': leverage
        }
        return self.session.post(url, params=params)