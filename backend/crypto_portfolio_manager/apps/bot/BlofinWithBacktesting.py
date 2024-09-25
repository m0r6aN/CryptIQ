import ccxt
import pandas as pd
from typing import List, Dict
from datetime import datetime, timedelta

class BlofimTradingBot:
    # ... [Previous code remains the same] ...

    def backtest(self, start_date: str, end_date: str, initial_balance: float = 100000):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        results = {}
        for symbol in self.symbols:
            print(f"Backtesting {symbol}...")
            
            # Fetch historical data
            ohlcv = self.exchange.fetch_ohlcv(
                symbol, 
                self.timeframe, 
                int(start.timestamp() * 1000),
                int(end.timestamp() * 1000)
            )
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            balance = initial_balance
            position = {'side': None, 'amount': 0, 'entry_price': 0}
            trades = []
            
            for i in range(self.c, len(df)):
                current_data = df.iloc[:i+1]
                atr = self.calculate_atr(current_data)
                atr_trailing_stop = self.calculate_atr_trailing_stop(current_data, atr)
                signal = self.check_cross(current_data.iloc[-2:], atr_trailing_stop)
                
                current_price = current_data['close'].iloc[-1]
                
                if signal == 'buy' and position['side'] != 'long':
                    if position['side'] == 'short':
                        # Close short position
                        pnl = position['amount'] * (position['entry_price'] - current_price)
                        balance += pnl
                        trades.append({
                            'timestamp': current_data.index[-1],
                            'type': 'close_short',
                            'price': current_price,
                            'amount': position['amount'],
                            'pnl': pnl
                        })
                        position = {'side': None, 'amount': 0, 'entry_price': 0}
                    
                    # Open long position
                    amount = (balance * self.leverage) / current_price
                    position = {'side': 'long', 'amount': amount, 'entry_price': current_price}
                    trades.append({
                        'timestamp': current_data.index[-1],
                        'type': 'open_long',
                        'price': current_price,
                        'amount': amount
                    })
                
                elif signal == 'sell' and position['side'] != 'short':
                    if position['side'] == 'long':
                        # Close long position
                        pnl = position['amount'] * (current_price - position['entry_price'])
                        balance += pnl
                        trades.append({
                            'timestamp': current_data.index[-1],
                            'type': 'close_long',
                            'price': current_price,
                            'amount': position['amount'],
                            'pnl': pnl
                        })
                        position = {'side': None, 'amount': 0, 'entry_price': 0}
                    
                    # Open short position
                    amount = (balance * self.leverage) / current_price
                    position = {'side': 'short', 'amount': amount, 'entry_price': current_price}
                    trades.append({
                        'timestamp': current_data.index[-1],
                        'type': 'open_short',
                        'price': current_price,
                        'amount': amount
                    })
            
            # Close any open position at the end of the backtest
            if position['side'] is not None:
                final_price = df['close'].iloc[-1]
                if position['side'] == 'long':
                    pnl = position['amount'] * (final_price - position['entry_price'])
                else:
                    pnl = position['amount'] * (position['entry_price'] - final_price)
                balance += pnl
                trades.append({
                    'timestamp': df.index[-1],
                    'type': f"close_{position['side']}",
                    'price': final_price,
                    'amount': position['amount'],
                    'pnl': pnl
                })
            
            trades_df = pd.DataFrame(trades)
            results[symbol] = {
                'final_balance': balance,
                'total_return': (balance - initial_balance) / initial_balance * 100,
                'trades': trades_df
            }
        
        return results

    def print_backtest_results(self, results: Dict):
        for symbol, data in results.items():
            print(f"\nBacktest Results for {symbol}")
            print(f"Final Balance: ${data['final_balance']:.2f}")
            print(f"Total Return: {data['total_return']:.2f}%")
            print(f"Number of Trades: {len(data['trades'])}")
            
            if not data['trades'].empty:
                winning_trades = data['trades'][data['trades']['pnl'] > 0]
                losing_trades = data['trades'][data['trades']['pnl'] < 0]
                win_rate = len(winning_trades) / len(data['trades']) * 100
                print(f"Win Rate: {win_rate:.2f}%")
                print(f"Average Winning Trade: ${winning_trades['pnl'].mean():.2f}")
                print(f"Average Losing Trade: ${losing_trades['pnl'].mean():.2f}")
                print(f"Largest Winning Trade: ${winning_trades['pnl'].max():.2f}")
                print(f"Largest Losing Trade: ${losing_trades['pnl'].min():.2f}")
            
            print("\nTrade History:")
            print(data['trades'])

if __name__ == "__main__":
   if __name__ == "__main__":
    API_KEY = 'f2be02aeaece4cbf8bd2fadee5e4654b'
    SECRET = 'e892ca4192854dfa82e4cb6fb6d77cee'
    SYMBOLS = ['BTC-USDT', 'ETH-USDT', 'XRP-USDT','FIL-USDT', 'AR-USDT', 'SOL-USDT','SUI-USDT', 'THETA-USDT','SUI-USDT']  # Add or remove symbols as needed
    
    bot = BlofimTradingBot(API_KEY, SECRET, SYMBOLS)
    
    # Run backtest
    start_date = '2023-01-01'
    end_date = '2024-09-21'
    backtest_results = bot.backtest(start_date, end_date)
    bot.print_backtest_results(backtest_results)
    
    # Uncomment the following line to run the live trading bot
    # bot.run()