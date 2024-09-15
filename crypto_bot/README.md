# Automated Crypto Trading Bot

This project is an automated crypto trading bot designed to analyze market conditions and execute trades based on various strategies. The bot supports multiple market strategies such as trending, sideways, breakout, and more, each using different indicators to maximize profitability.

## Features

- **Multiple Strategies**: Support for strategies like Momentum, Ichimoku Cloud, Bollinger Reversion, ATR, RSI Divergence, and more.
- **Leverage Trading**: The bot can trade with up to 50x leverage when conditions are favorable.
- **Dynamic Strategy Selection**: Based on market conditions, the bot dynamically selects and prioritizes the best strategies.
- **Backtesting**: Simulate the bot's performance on historical data to evaluate and optimize strategies.
- **Risk Management**: Calculate position sizes based on risk percentages and leverage, ensuring proper risk management.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/crypto-trading-bot.git
    ```

2. Navigate into the project directory:

    ```bash
    cd crypto-trading-bot
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up API keys for exchanges (e.g., Binance) and Token Metrics if applicable.

## Usage

### Running the Bot

You can run the trading bot by executing the main Python script:

```bash
python main.py
```

Backtesting
To run backtesting for a strategy, use the backtesting framework included in the backtesting folder:

```python
from backtesting.backtester import Backtester
from strategies.momentum_strategy import MomentumStrategy
import pandas as pd

# Load historical data into a DataFrame (e.g., CSV data)
data = pd.read_csv('historical_data.csv')

# Instantiate the strategy and backtester
strategy = MomentumStrategy()
backtester = Backtester(strategy, data)

# Run the backtest
backtester.run()
```

Project Structure

```bash
├── backtesting/
│   └── backtester.py          # Backtesting framework for simulating strategies
├── data/
│   └── data_fetcher.py        # Fetches data from APIs like Binance, Token Metrics
├── strategies/
│   ├── base_strategy.py       # Base class for all strategies
│   ├── momentum_strategy.py   # Example strategy: Momentum
│   └── ...                    # Other strategies like Bollinger, RSI, etc.
├── tasks/
│   └── ...                    # Task-based architecture for executing workflows
├── utils/
│   ├── indicators.py          # Utility functions to calculate indicators
│   └── ...                    # Other utilities
├── main.py                    # Entry point for running the bot
└── requirements.txt           # Python dependencies
```

## Strategies
- Momentum Strategy: Trades based on overbought and oversold RSI levels.
- Ichimoku Cloud Strategy: Uses the Ichimoku Cloud for trend identification.
- Breakout Strategy: Detects breakouts above resistance or below support levels.
- Bollinger Reversion Strategy: Uses Bollinger Bands to trade in ranging markets.
- RSI Divergence Strategy: Trades based on divergence between price action and RSI.
- Trending Strategy: Follows trends using moving averages.
- ATR Strategy:
- Correlation Strategy:
- Engulfing Strategy:
- Grid Ranging Strategy:
- Leverage Strategy: Decides when and how much levergage to use. Up to 50x. 
- Momentum Strategy:
- Moving Average Crossover Strategy:

## Risk Management
The bot calculates position sizes based on the trader's available balance and the leverage they wish to apply. The calculate_position_size function ensures that risk is minimized while maximizing returns based on the defined strategy.

## Customization
You can easily modify or add new strategies by creating a new class that inherits from BaseStrategy and implementing the on_data method. 
Example:

```python
from strategies.base_strategy import BaseStrategy

class MyCustomStrategy(BaseStrategy):
    def on_data(self, data):
        # Implement your strategy logic here
        pass
```

## Contribution
Feel free to submit issues, fork the repo, and make pull requests. All contributions are welcome!