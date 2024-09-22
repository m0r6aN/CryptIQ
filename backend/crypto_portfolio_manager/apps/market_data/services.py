# apps/market_data/services.py

import numpy as np
import logging

from backend.crypto_portfolio_manager.apps.market_data.data_fetcher import fetch_historical_prices, fetch_market_data
from crypto_portfolio_manager.apps.ai_engine.sentiment_analysis import get_sentiment_analysis

def calculate_market_volatility(coin):
    # Fetch historical price data for the coin (replace with actual data source)
    historical_prices = fetch_historical_prices(coin)

    # Calculate daily returns
    returns = np.diff(historical_prices) / historical_prices[:-1]

    # Calculate the standard deviation of returns as a measure of volatility
    volatility = np.std(returns)
    
    return volatility

def get_current_market_state(coin):
    price = get_current_price(coin)
    sentiment = get_sentiment_analysis(coin)
    
    return np.array([price, sentiment])

def get_current_price(coin):
    market_data = fetch_market_data(coin)
    return market_data[coin]['usd'] if market_data else np.random.rand() * 50000

def fetch_price_trend(coin):
    # Fetch historical prices (e.g., last 30 days)
    prices = fetch_historical_prices(coin, days=30)

    # Calculate moving averages or other indicators to determine the trend
    short_term_avg = np.mean(prices[-5:])  # Last 5 days moving average
    long_term_avg = np.mean(prices[-30:])  # Last 30 days moving average

    if short_term_avg > long_term_avg:
        return 'uptrend'
    elif short_term_avg < long_term_avg:
        return 'downtrend'
    else:
        return 'neutral'