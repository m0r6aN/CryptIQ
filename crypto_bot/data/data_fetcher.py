import pandas as pd
import ccxt
import requests
import time

class DataFetcher:
    def __init__(self, exchange_name='binance', token_metrics_api_key=None):
        self.exchange = getattr(ccxt, exchange_name)()
        self.token_metrics_api_key = token_metrics_api_key
        self.token_metrics_base_url = 'https://api.tokenmetrics.com/v1'

    def fetch_exchange_data(self, symbol='BTC/USDT', timeframe='1m', limit=1000):
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        data['datetime'] = pd.to_datetime(data['timestamp'], unit='ms')
        return data

    def fetch_token_metrics_data(self, symbol='BTC'):
        headers = {'Authorization': f'Bearer {self.token_metrics_api_key}'}
        endpoint = f'{self.token_metrics_base_url}/assets/{symbol}/indicators'
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            return df
        else:
            # Handle errors or retries as needed
            time.sleep(1)
            return self.fetch_token_metrics_data(symbol)

    def fetch_data(self, symbol='BTC/USDT', timeframe='1m', limit=1000):
        exchange_data = self.fetch_exchange_data(symbol, timeframe, limit)
        if self.token_metrics_api_key:
            token_metrics_symbol = symbol.split('/')[0]
            tm_data = self.fetch_token_metrics_data(token_metrics_symbol)
            data = pd.merge_asof(exchange_data.sort_values('datetime'),
                                 tm_data.sort_values('datetime'),
                                 on='datetime', direction='nearest')
            return data
        else:
            return exchange_data
