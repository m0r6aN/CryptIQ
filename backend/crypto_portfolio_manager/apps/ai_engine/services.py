# ai_engine/services.py

import numpy as np
from sklearn.linear_model import LinearRegression
from celery import shared_task
import logging

from crypto_portfolio_manager.apps.portfolio.services import calculate_amount_to_buy, calculate_amount_to_sell
from crypto_portfolio_manager.apps.trading.services import execute_trade
from crypto_portfolio_manager.apps.ai_engine.predictive_models import predict_price, train_reinforcement_agent
from crypto_portfolio_manager.apps.ai_engine.sentiment_analysis import fetch_sentiment_over_time, generate_ai_recommendations_for_user, get_sentiment_analysis
from crypto_portfolio_manager.apps.market_data.services import calculate_market_volatility, fetch_price_trend, get_current_market_state
from crypto_portfolio_manager.apps.portfolio.models import Portfolio, User
from crypto_portfolio_manager.apps.trading.models import Trade

def ai_stop_loss_take_profit(user, coin):
    sentiment = get_sentiment_analysis(coin)
    volatility = calculate_market_volatility(coin)  # Fetch volatility data from APIs

    # Set stop-loss and take-profit based on market conditions
    if sentiment > 0.7:
        stop_loss = -0.05  # More aggressive if sentiment is positive
        take_profit = 0.15
    elif volatility > 0.8:
        stop_loss = -0.02  # Tighter stop loss in volatile markets
        take_profit = 0.10
    else:
        stop_loss = -0.10  # Standard conservative values
        take_profit = 0.20

    return {'stop_loss': stop_loss, 'take_profit': take_profit}

def optimize_trades(user):
    # Fetch past trades
    trade_history = Trade.objects.filter(user=user)
    
    # Create dataset from trade history (inputs: buy/sell prices, outputs: profit/loss)
    prices = np.array([trade.price for trade in trade_history]).reshape(-1, 1)
    outcomes = np.array([trade.profit_or_loss for trade in trade_history])

    # Train a simple model to predict profit based on price
    model = LinearRegression()
    model.fit(prices, outcomes)
    
    # Use model to suggest optimal trade price range
    suggested_price_range = model.predict([[min(prices)], [max(prices)]])
    
    return suggested_price_range

def place_trade_with_ai_risk_management(user, coin, amount, trade_type):
    risk_params = ai_stop_loss_take_profit(user, coin)
    # Execute the trade with the AI-driven stop-loss/take-profit levels
    trade = execute_trade(coin, amount, trade_type, stop_loss=risk_params['stop_loss'], take_profit=risk_params['take_profit'])
    
    return trade

def ai_trade_timing(coin):
    sentiment_data = fetch_sentiment_over_time(coin)  # Fetch historical sentiment data
    latest_sentiment = sentiment_data[-1]
    
    if latest_sentiment > 0.8:
        return 'Buy'
    elif latest_sentiment < 0.3:
        return 'Sell'
    else:
        return 'Hold'

def ai_trade_agent(user):
    model = train_reinforcement_agent()
    
    # Simulate a trade and get the recommended action
    action = model.predict(observation=get_current_market_state())
    
    return action

def generate_ai_dashboard(user):
    portfolio = Portfolio.objects.get(user=user)
    coins = portfolio.coins.all()

    dashboard_data = {}
    for coin in coins:
        sentiment = get_sentiment_analysis(coin.symbol)
        prediction = predict_price(coin.symbol)
        dashboard_data[coin.symbol] = {
            'sentiment': sentiment,
            'price_prediction': prediction
        }

    return dashboard_data

def ai_momentum_strategy(user, coin):
    sentiment = get_sentiment_analysis(coin)
    price_trend = fetch_price_trend(coin)  # Calculate based on moving averages or trend lines

    if sentiment > 0.7 and price_trend == 'uptrend':
        return 'Buy'
    elif sentiment < 0.3 and price_trend == 'downtrend':
        return 'Sell'
    else:
        return 'Hold'
    
   
@shared_task
def auto_rebalance(user_id):
    try:
        user = User.objects.get(id=user_id)
        recommendations = generate_ai_recommendations_for_user(user)
        for coin in recommendations['underperforming']:
            execute_trade(coin, 'sell', calculate_amount_to_sell(coin))
            execute_trade(recommendations['rising_trends'][0], 'buy', calculate_amount_to_buy(coin))
        return f'Rebalanced portfolio for {user.username}'
    except Exception as e:
        logging.error(f"Error during auto-rebalance for user {user_id}: {e}")
