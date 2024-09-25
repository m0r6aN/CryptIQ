import pandas as pd
import matplotlib.pyplot as plt
from strategies.base_strategy import BaseStrategy

class Backtester:
    def __init__(self, strategy: BaseStrategy, data: pd.DataFrame, initial_balance: float = 10000):
        self.strategy = strategy
        self.data = data.reset_index(drop=True)
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.position = None
        self.entry_price = None
        self.trade_log = []

    def run(self):
        for index, row in self.data.iterrows():
            signal = self.strategy.on_data(self.data.iloc[:index+1])
            self.execute_trade(signal, row)

        self.generate_report()

    def execute_trade(self, signal, data_row):
        price = data_row['close']
        datetime = data_row['datetime']

        if signal == 'buy':
            if self.position is None:
                self.position = 'long'
                self.entry_price = price
                self.trade_log.append({
                    'datetime': datetime,
                    'action': 'buy',
                    'price': price,
                    'balance': self.current_balance
                })
        elif signal == 'sell':
            if self.position == 'long':
                profit = (price - self.entry_price)
                self.current_balance += profit
                self.trade_log.append({
                    'datetime': datetime,
                    'action': 'sell',
                    'price': price,
                    'balance': self.current_balance
                })
                self.position = None
                self.entry_price = None
        elif signal == 'short':
            if self.position is None:
                self.position = 'short'
                self.entry_price = price
                self.trade_log.append({
                    'datetime': datetime,
                    'action': 'short',
                    'price': price,
                    'balance': self.current_balance
                })
        elif signal == 'cover':
            if self.position == 'short':
                profit = (self.entry_price - price)
                self.current_balance += profit
                self.trade_log.append({
                    'datetime': datetime,
                    'action': 'cover',
                    'price': price,
                    'balance': self.current_balance
                })
                self.position = None
                self.entry_price = None

    def generate_report(self):
        trades = pd.DataFrame(self.trade_log)
        trades.set_index('datetime', inplace=True)
        plt.figure(figsize=(12, 6))
        plt.plot(trades['balance'])
        plt.title('Equity Curve')
        plt.xlabel('Time')
        plt.ylabel('Balance')
        plt.grid(True)
        plt.show()

        total_return = self.current_balance - self.initial_balance
        print(f"Total Return: {total_return:.2f}")

        # Additional performance metrics
        returns = trades['balance'].pct_change().fillna(0)
        sharpe_ratio = (returns.mean() / returns.std()) * (252 ** 0.5)
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

        max_drawdown = (trades['balance'].cummax() - trades['balance']).max()
        print(f"Max Drawdown: {max_drawdown:.2f}")
