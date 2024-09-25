import logging
import os
import sys
import pandas as pd
import ccxt

# Configure logging and paths
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from utils.api_client import APIClient

TOKEN_METRICS_API_KEY = os.getenv("TOKEN_METRICS_API_KEY")

class DataFetcher:
    def __init__(self, exchange_name='blofin', token_metrics_api_key=None):
        self.exchange = getattr(ccxt, exchange_name)()
        self.token_metrics_api_key = token_metrics_api_key
        self.token_metrics_base_url = 'https://api.tokenmetrics.com/v1'

    def fetch_exchange_data(self, symbol='BTC/USDT', timeframe='1m', limit=1000):
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        data['datetime'] = pd.to_datetime(data['timestamp'], unit='ms')
        return data

    def fetch_ohlcv_data(self, symbol='BTC/USDT', timeframe='1m', limit=1000):
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
        
    async def get_historical_data(self, session, symbol, timeframe, limit, aggregate):
        url = f"https://min-api.cryptocompare.com/data/v2/histo{timeframe}"
        params = {'fsym': symbol, 'tsym': 'USD', 'limit': limit, 'aggregate': aggregate}
        print(f'Getting historical Data for {symbol}')

        try:
            data = await APIClient.rate_limited_request(session, url, params)
            if data['Response'] == 'Success':
                print('Success')
                df = pd.DataFrame(data['Data']['Data'])
                df['datetime'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('datetime', inplace=True)
                df.rename(columns={'volumefrom': 'volume'}, inplace=True)
                return df[['open', 'high', 'low', 'close', 'volume']]
            else:
                print('Failure')
                logging.error(f"Error fetching data for {symbol}: {data['Message']}")
                return None
        except Exception as e:
            logging.error(f"Request failed for {symbol}: {e}")
            return None

    @staticmethod
    async def get_top_coins(session, limit):
        print('Getting top coins')
        url = 'https://min-api.cryptocompare.com/data/top/mktcapfull'
        params = {'limit': limit, 'tsym': 'USD'}
        try:
            data = await APIClient.rate_limited_request(session, url, params)
            if data['Message'] == 'Success':
                return [coin_data['CoinInfo']['Name'] for coin_data in data['Data']]
            else:
                logging.error(f"Error fetching top coins: {data['Message']}")
                return []
        except Exception as e:
            logging.error(f"Request failed: {e}")
            return []

    @staticmethod
    async def filter_top_coins(symbols, session):
        url = 'https://min-api.cryptocompare.com/data/pricemultifull'
        params = {'fsyms': ','.join(symbols), 'tsyms': 'USD'}
        async with session.get(url, params=params) as response:
            data = await response.json()

        filtered_coins = []
        for symbol, info in data['RAW'].items():
            usd_data = info['USD']

            # Example filtering criteria
            if (usd_data['CHANGEPCT24HOUR'] > 5 or usd_data['CHANGEPCT24HOUR'] < -5) and \
                    usd_data['VOLUME24HOUR'] > 1000000 and \
                    usd_data['MKTCAP'] > 1000000000:
                filtered_coins.append(symbol)

        return filtered_coins

    async def get_multi_timeframe_data(self, session, symbol):
        timeframes = [
            ('hour', 24, 1),  # 1-day data with 1-hour aggregation
            ('hour', 168, 4),  # 1-week data with 4-hour aggregation
            ('day', 30, 1)  # 1-month data with 1-day aggregation
        ]

        data = {}
        for tf, limit, aggregate in timeframes:
            df = await self.get_historical_data(session, symbol, tf, limit, aggregate)
            if df is not None:
                data[tf] = df

        return data

    @staticmethod
    async def get_trading_signals(session, symbol):
        url = 'https://min-api.cryptocompare.com/data/tradingsignals/intotheblock/latest'
        params = {'fsym': symbol}
        try:
            data = await APIClient.rate_limited_request(session, url, params)
            if data['Response'] == 'Success':
                return data['Data']
            else:
                logging.error(f"Error fetching trading signals for {symbol}: {data['Message']}")
                return None
        except Exception as e:
            logging.error(f"Request failed for trading signals of {symbol}: {e}")
            return None