from backend.crypto_portfolio_manager.apps.portfolio.models import Portfolio, User
import requests
from fbprophet import Prophet
import pandas as pd
from stable_baselines3 import PPO
from transformers import pipeline
from celery import shared_task

def get_sentiment_analysis(coin):
    # Example using LunarCrush API
    api_url = f'https://api.lunarcrush.com/v2/assets?symbol={coin}&data=sentiment'
    api_key = 'your_lunarcrush_api_key'
    
    response = requests.get(api_url, headers={'Authorization': f'Bearer {api_key}'})
    if response.status_code == 200:
        data = response.json()
        sentiment = data['data'][0]['sentiment']  # Adjust based on actual API response
        return sentiment
    else:
        return None
    
def suggest_portfolio_rebalancing(user):
    portfolio = Portfolio.objects.get(user=user)
    coins = portfolio.coins.all()
    
    recommendations = {
        'underperforming': [],
        'rising_trends': [],
        'price_predictions': {}
    }
    
    for coin in coins:
        sentiment = get_sentiment_analysis(coin.symbol)
        if sentiment and sentiment > 0.5:
            recommendations['rising_trends'].append(coin.symbol)
        else:
            recommendations['underperforming'].append(coin.symbol)
        
        # Add price prediction
        price_prediction = predict_price(coin.symbol)
        recommendations['price_predictions'][coin.symbol] = price_prediction
    
    return recommendations

def execute_rebalancing_strategy(strategy):
    # Example: Rebalance the portfolio based on a predefined strategy
    if strategy == 'conservative':
        return 'Sell high-risk assets and buy stablecoins'
    elif strategy == 'aggressive':
        return 'Sell stablecoins and buy high-risk assets'
    else:
        return 'No action needed'   

def hedge_risk(user):
    portfolio = Portfolio.objects.get(user=user)
    total_risk = calculate_portfolio_risk(portfolio)
    
    if total_risk > threshold:
        # Suggest or place a hedge (e.g., buy stablecoins)
        hedge_action = "Buy USDT to hedge against BTC downturn"
        return hedge_action
    return "No hedge needed"
