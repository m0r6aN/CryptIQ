import asyncio
import logging
import requests
import aiohttp
import os
from config.settings import API_KEY, API_SECRET, EXCHANGE_URL

MAX_RETRIES = 5
INITIAL_BACKOFF = 2  # Initial backoff time in seconds
MAX_CONCURRENT_REQUESTS = 2  # Reduced to 1 for very conservative rate limiting
DELAY_BETWEEN_REQUESTS = 1  # 1 second delay between requests
CRYPTOCOMPARE_API_KEY=os.getenv("CRYPTOCOMPARE_API_KEY")

# Headers for CryptCompare API requests
CRYPTOCOMPARE_API_HEADERS = {'Authorization': f'Apikey {CRYPTOCOMPARE_API_KEY}'}

# Semaphore for rate limiting
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    
    async def rate_limited_request(session, url, params=None):
        async with semaphore:
            for attempt in range(MAX_RETRIES):
                try:
                    await asyncio.sleep(DELAY_BETWEEN_REQUESTS)  # Fixed delay between requests
                # print(f'Calling rate limited: {url}')
                    async with session.get(url, headers=CRYPTOCOMPARE_API_HEADERS, params=params) as response:
                        if response.status == 429:  # Too Many Requests
                            raise aiohttp.ClientResponseError(response.request_info, response.history, status=429)
                        response.raise_for_status()
                        return await response.json()
                except aiohttp.ClientResponseError as e:
                    if e.status == 429 or (500 <= e.status < 600):
                        backoff = INITIAL_BACKOFF * (2 ** attempt)
                        logging.warning(f"Rate limit hit or server error. Retrying in {backoff} seconds...")
                        await asyncio.sleep(backoff)
                    else:
                        raise
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(INITIAL_BACKOFF * (2 ** attempt))
                    else:
                        raise
            raise Exception(f"Failed after {MAX_RETRIES} attempts")