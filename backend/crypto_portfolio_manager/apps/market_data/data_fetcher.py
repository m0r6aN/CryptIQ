import logging
import requests
import numpy as np
import crypto_portfolio_manager.settings as settings

LUNAR_CRUSH_API_BASE_URL = settings.LUNAR_CRUSH_API_BASE_URL
COIN_GECKO_API_BASE_URL = settings.COIN_GECKO_API_BASE_URL

def fetch_market_data(symbol):
    try:
        response = requests.get(f'{LUNAR_CRUSH_API_BASE_URL}/v3/simple/price', params={
            'ids': symbol,
            'vs_currencies': 'usd',
        })
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching market data for {symbol}: {e}")
        return None  # Return None or a default value in case of error
    
def fetch_historical_prices(coin, days=100):
    # Fetch historical price data for the last 'days' days
    try:
        response = requests.get(f'{COIN_GECKO_API_BASE_URL}/coins/{coin}/market_chart', params={
            'vs_currency': 'usd',
            'days': days,
        })
        response.raise_for_status()
        prices = response.json()['prices']
        return [price[1] for price in prices]  # Extract the price values
    except requests.RequestException as e:
        logging.error(f"Error fetching historical prices for {coin}: {e}")
        return np.random.rand(100)  # Fallback to random data for now
    
    