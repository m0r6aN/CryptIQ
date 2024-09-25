import ccxt
import pandas as pd
import numpy as np
import time
from typing import List, Dict

class BlofinTradingBot:
    def __init__(self, api_key: str, secret: str, symbols: List[str], timeframe: str = '6h',
                 a: float = 1.0, c: int = 10, h: bool = False, leverage: float = 1.0):
        self.exchange = ccxt.blofin({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        self.symbols = symbols
        self.timeframe = timeframe
        self.a = a
        self.c = c
        self.h = h
        self.leverage = leverage
        self.positions: Dict[str, Dict] = {symbol: {} for symbol in symbols}

    def fetch_ohlcv(self, symbol: str) -> pd.DataFrame:
        ohlcv = self.exchange.fetch_ohlcv(symbol, self.timeframe, limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df

    def check_cross(self, df: pd.DataFrame, atr_trailing_stop: float) -> str:
        current_close = df['close'].iloc[-1]
        previous_close = df['close'].iloc[-2]
        
        if previous_close <= atr_trailing_stop and current_close > atr_trailing_stop:
            return 'buy'
        elif previous_close >= atr_trailing_stop and current_close < atr_trailing_stop:
            return 'sell'
        else:
            return 'hold'

    def execute_trade(self, symbol: str, side: str, amount: float):
        try:
            if side == 'buy':
                print(f"Buying {amount} of {symbol}")
                self.exchange.create_market_buy_order(symbol, amount)
            elif side == 'sell':
                print(f"Selling {amount} of {symbol}")
                self.exchange.create_market_sell_order(symbol, amount)
        except Exception as e:
            print(f"Error executing trade for {symbol}: {e}")

    def run(self):
        while True:
            for symbol in self.symbols:
                try:
                    df = self.fetch_ohlcv(symbol)
                    atr = self.calculate_atr(df)
                    atr_trailing_stop = self.calculate_atr_trailing_stop(df, atr)
                    signal = self.check_cross(df, atr_trailing_stop)
                    
                    current_position = self.positions.get(symbol, {})
                    
                    if signal == 'buy' and current_position.get('side') != 'long':
                        amount = self.calculate_position_size(symbol)
                        self.execute_trade(symbol, 'buy', amount)
                        self.positions[symbol] = {'side': 'long', 'amount': amount}
                        print(f"Opened long position for {symbol}")
                    
                    elif signal == 'sell' and current_position.get('side') != 'short':
                        if current_position.get('side') == 'long':
                            self.execute_trade(symbol, 'sell', current_position['amount'])
                            print(f"Closed long position for {symbol}")
                        
                        amount = self.calculate_position_size(symbol)
                        self.execute_trade(symbol, 'sell', amount)
                        self.positions[symbol] = {'side': 'short', 'amount': amount}
                        print(f"Opened short position for {symbol}")
                
                except Exception as e:
                    print(f"Error processing {symbol}: {e}")
            
            time.sleep(60)  # Wait for 1 minute before the next iteration

if __name__ == "__main__":
    API_KEY = 'f2be02aeaece4cbf8bd2fadee5e4654b'
    SECRET = 'e892ca4192854dfa82e4cb6fb6d77cee'
    SYMBOLS = ['BTC-USDT', 'ETH-USDT', 'XRP-USDT','FIL-USDT', 'AR-USDT', 'SOL-USDT','SUI-USDT', 'THETA-USDT','SUI-USDT']  # Add or remove symbols as needed
    
    bot = BlofimTradingBot(API_KEY, SECRET, SYMBOLS)
    bot.run()