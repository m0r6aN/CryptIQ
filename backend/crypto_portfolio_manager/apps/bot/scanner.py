from dotenv import load_dotenv
import sys
import os
import logging
import asyncio
import nest_asyncio
import ccxt
import pandas as pd
import platform
from aiohttp import ClientSession, TCPConnector
from playsound import playsound
import talib

# Configure logging and paths
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from utils.data_fetcher import process_coin
from utils.shared import DataFetcher

FINISHED_SOUND_FILE = os.path.join(project_root, 'audio', 'tada.mp3')
EXIT_FOUND_SOUND = os.path.join(project_root, 'audio', 'windows-critical-stop.mp3')

# Load environment variables
load_dotenv()

CRYPTOCOMPARE_API_KEY = os.getenv('CRYPTOCOMPARE_API_KEY')
TOP_N_COINS = 100
TIMEFRAME = 'hour'
LIMIT = 200
MAX_RETRIES = 5
INITIAL_BACKOFF = 2  # Initial backoff time in seconds
MAX_CONCURRENT_REQUESTS = 2  # Reduced to 1 for very conservative rate limiting
DELAY_BETWEEN_REQUESTS = 1  # 1 second delay between requests

# Headers for API requests
HEADERS = {'Authorization': f'Apikey {CRYPTOCOMPARE_API_KEY}'}

# Windows-specific event loop policy
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
nest_asyncio.apply()

def get_blofin_holdings(type: str='future'):
    exchange = ccxt.blofin({
        'apiKey': os.getenv('BLOFIN_API_KEY'),
        'secret': os.getenv('BLOFIN_SECRET'),
        'password': os.getenv('BLOFIN_PASSWORD'),
        'enableRateLimit': True,
        'options': {'defaultType': type}
    })
    try:
        balance = exchange.fetch_balance()
        positions = balance.get('info', {}).get('positions', [])
        holdings = [position['symbol'].split(':')[0] for position in positions if float(position['positionAmt']) != 0]
        logging.info(f"Current holdings: {', '.join(holdings)}")
        return holdings
    except Exception as e:
        logging.error(f"Error fetching Blofin holdings: {e}")
        return []

async def interruptible_sleep(seconds):
    try:
        await asyncio.sleep(seconds)
    except asyncio.CancelledError:
        raise KeyboardInterrupt

async def main():
    try:
        connector = TCPConnector(limit_per_host=MAX_CONCURRENT_REQUESTS)
        async with ClientSession(connector=connector) as session:
            while True:
                top_x_coins = await DataFetcher.get_top_coins(session, TOP_N_COINS)
                filtered_coins = await DataFetcher.filter_top_coins(top_x_coins, session)
                holdings = get_blofin_holdings()                
                
                results = []
                
                for symbol in filtered_coins:
                    result = await process_coin(session, symbol, TIMEFRAME, LIMIT)  # Ensure LIMIT is passed here
                    if result:
                        results.append(result)
                        logging.info(f"Processed {symbol}")

                for result in results:
                    if result['Signal'] == 'Exit' and result['Symbol'] in holdings:
                        try:
                            playsound(EXIT_FOUND_SOUND)
                            logging.info(f"Exit signal for held coin: {result['Symbol']}")
                        except Exception as e:
                            logging.error(f"Error playing exit sound: {e}")

                results_df = pd.DataFrame(results)
                timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
                filename = f'crypto_signals_{timestamp}.csv'
                logging.info(results_df)
                results_df.to_csv(filename, index=False)

                logging.info(f"Results saved to {filename}")

                try:
                    playsound(FINISHED_SOUND_FILE)
                except Exception as e:
                    logging.error(f"Error playing finished sound: {e}")

                logging.info("Waiting for 10 minutes before next run...")
                
                try:
                    await asyncio.wait_for(interruptible_sleep(600), timeout=600)
                except asyncio.TimeoutError:
                    pass  # This is expected, we just use it to check for interrupts regularly

    except KeyboardInterrupt:
        logging.info("Script interrupted by user. Exiting...")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    asyncio.run(main())