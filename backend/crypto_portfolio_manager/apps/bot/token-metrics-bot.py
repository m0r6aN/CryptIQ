# Import Dependencies
import os
import time
import pandas as pd
import requests
import alpaca_trade_api as tradeapi

# API Credentials
TOKEN_METRICS_API_KEY=os.getenv("TOKEN_METRICS_API_KEY")
api = tradeapi.REST(TOKEN_METRICS_API_KEY,'https://api.tokenmetrics.com')

# Define crypto related variables
symbol = ''
qty_per_trade = 1

# Check Whether Account Currently Holds Symbol
def check_positions(symbol):
    positions = api.list_positions()
    for p in positions:
        if p.symbol == symbol:
            return float(p.qty)
    return 0
  
def fetch_token_metrics_data(self, symbol='BTC'):
        headers = {'Authorization': f'Bearer {self.token_metrics_api_key}'}
        endpoint = f'{self.token_metrics_base_url}/assets/{symbol}/indicators'
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
            return df
        else:
            # Handle errors or retries as needed
            time.sleep(1)
            return self.fetch_token_metrics_data(symbol)
  
  # Supertrend Indicator Bot Function
def supertrend_bot(bar):
    try:
        # Get the Latest Data
        dataframe = api.get_crypto_bars(symbol, tradeapi.TimeFrame(1, tradeapi.TimeFrameUnit.Minute)).df
        dataframe = dataframe[dataframe.exchange == 'CBSE']
        sti = ta.supertrend(dataframe['high'], dataframe['low'], dataframe['close'], 7, 3)
        dataframe = pd.concat([dataframe, sti], axis=1)

        position = check_positions(symbol=symbol)
        should_buy = bar["c"] > dataframe["SUPERT_7_3.0"][-1]
        should_sell = bar["c"] < dataframe["SUPERT_7_3.0"][-1]
        print(f"Price: {bar["c"]}")
        print("Super Trend Indicator: {}".format(dataframe["SUPERT_7_3.0"][-1]))
        print(f"Position: {position} | Should Buy: {should_buy}")

        # Check if No Position and Buy Signal is True
        if position == 0 and should_buy == True:
            api.submit_order(symbol, qty=qty_per_trade, side='buy')
            message = f'Symbol: {symbol} | Side: Buy | Quantity: {qty_per_trade}'
            print(message)
            # send_mail(message)

        # Check if Long Position and Sell Signal is True
        elif position > 0 and should_sell == True:
            api.submit_order(symbol, qty=qty_per_trade, side='sell')
            message = f'Symbol: {symbol} | Side: Sell | Quantity: {qty_per_trade}'
            print(message)
            # send_mail(message)
        print("-"*20)

    except Exception as e:
        print (e)
        # send_mail(f"Trading Bot failed due to {e}")
