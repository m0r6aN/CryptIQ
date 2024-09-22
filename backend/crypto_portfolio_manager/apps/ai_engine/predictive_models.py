# apps/ai_engine/predictive_models.py

import prophet
import pandas as pd

from stable_baselines3 import PPO

from crypto_portfolio_manager.apps.market_data.data_fetcher import fetch_historical_prices
from crypto_portfolio_manager.apps.ai_engine.custom_trading_env import create_custom_trading_env

def train_reinforcement_agent():
    # Define your environment (custom trading environment needed)
    env = create_custom_trading_env()

    # Initialize the agent
    model = PPO('MlpPolicy', env, verbose=1)

    # Train the agent
    model.learn(total_timesteps=10000)
    
    return model

def predict_price(coin):
    data = fetch_historical_prices(coin)
    df = pd.DataFrame(data)
    
    model = prophet()
    model.fit(df)
    
    # Forecasting the next 7 days
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)
    
    return forecast[['ds', 'yhat']]  # Predicted price



