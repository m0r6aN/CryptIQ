# apps/ai_engine/sentiment_analysis.py

import logging
import os
from transformers import pipeline
import numpy as np
import requests

from crypto_portfolio_manager.apps.ai_engine.predictive_models import predict_price
from crypto_portfolio_manager.apps.portfolio.models import Portfolio

LUNAR_CRUSH_API_KEY = os.getenv("LUNAR_CRUSH_API_KEY")
LUNAR_CRUSH_API_BASE_URL = 'https://lunarcrush.com/api4/'

# Increase the timeout to 60 seconds (default is 10)
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(timeout=60)
session.mount('https://', adapter)

sentiment_pipeline = pipeline('sentiment-analysis', model="D:\AI_Models\distilbert-base-uncased", use_auth_token=True)

def predict_future_sentiment(text):
    # Use Hugging Face's sentiment analysis pipeline to analyze the text
    sentiment_results = sentiment_pipeline(text)
    return sentiment_results

def get_sentiment_trends(user):
    coins = Portfolio.objects.get(user=user).coins.all()

    future_sentiments = {}
    for coin in coins:
        news_articles = fetch_coin_related_news(coin.symbol)
        predicted_sentiment = predict_future_sentiment(news_articles)
        future_sentiments[coin.symbol] = predicted_sentiment
    
    return future_sentiments

def fetch_coin_related_news(coin):
    try:
        url = f"{LUNAR_CRUSH_API_BASE_URL}news"
        params = {
            'key': LUNAR_CRUSH_API_KEY,
            'symbol': coin,
            'type': 'news'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()['data']  # Adjust based on actual API response
    except requests.RequestException as e:
        logging.error(f"Error fetching news for {coin}: {e}")
        return []
   
def get_sentiment_analysis(coin):
    try:
        api_url = f"{LUNAR_CRUSH_API_BASE_URL}assets?symbol={coin}&data=sentiment"
        api_key = LUNAR_CRUSH_API_KEY
        response = requests.get(api_url, headers={'Authorization': f'Bearer {api_key}'})
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return data['data'][0]['sentiment']
    except requests.exceptions.RequestException as e:
        # Log error
        logging.error(f"Error fetching sentiment data for {coin}: {e}")
        return None  # Return None or fallback value

def suggest_rebalancing(user):
    recommendations = generate_ai_recommendations_for_user(user)
    
    rebalance_actions = []
    for coin in recommendations['underperforming']:
        rebalance_actions.append(f'Sell {coin} and buy {recommendations["rising_trends"][0]}')
    
    return rebalance_actions

def generate_ai_recommendations_for_user(user):
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
        predicted_prices = predict_price(coin.symbol)
        recommendations['price_predictions'][coin.symbol] = predicted_prices.to_dict(orient='records')

    return recommendations

def fetch_sentiment_over_time(coin):
    # Example API call to fetch historical sentiment data
    api_url = f"{LUNAR_CRUSH_API_BASE_URL}/assets/sentiment-over-time?symbol={coin}"
    api_key = LUNAR_CRUSH_API_KEY
    
    response = requests.get(api_url, headers={'Authorization': f'Bearer {api_key}'})
    if response.status_code == 200:
        sentiment_data = response.json()['data']
        return [item['sentiment'] for item in sentiment_data]  # Adjust based on actual API response
    else:
        return []