# crypto_portfolio_manager/utils/data_fetcher.py

import asyncio
import logging
import sys
import os
import pandas as pd
import ccxt

# Configure logging and paths
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from utils.shared import DataFetcher
from utils.coin_analyzer import analyze_all_timeframes
from utils.api_client import APIClient

TOKEN_METRICS_API_KEY = os.getenv("TOKEN_METRICS_API_KEY")
TIMEFRAME = 'hour'
LIMIT = 200

# You can now use the DataFetcher class and other shared functions from shared.py

async def process_coin(session, symbol, timeframe, limit):
    try:
        # Add a timeout for API call
        data = await asyncio.wait_for(DataFetcher.get_historical_data(session, symbol, timeframe, limit), timeout=10)
        analyzed_data = analyze_all_timeframes(data)
        return analyzed_data
    except asyncio.TimeoutError:
        logging.error(f"Timeout when processing coin {symbol}")
    except Exception as e:
        logging.error(f"Error processing coin {symbol}: {e}")
    return None
