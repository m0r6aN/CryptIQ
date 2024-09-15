from strategies.trending_strategy import TrendingStrategy
from strategies.sideways_strategy import SidewaysStrategy
from strategies.leverage_strategy import LeverageStrategy
from utils.api_client import APIClient
from bot.trade_executor import TradeExecutor
from bot.risk_manager import RiskManager

if __name__ == "__main__":
    api_client = APIClient()
    trade_executor = TradeExecutor(api_client)
    risk_manager = RiskManager()
    
    trending_strategy = TrendingStrategy(trade_executor, risk_manager)
    sideways_strategy = SidewaysStrategy(trade_executor, risk_manager)
    leverage_strategy = LeverageStrategy(trade_executor, risk_manager)

    price_data = api_client.get_price_data()

    if trending_strategy.should_enter_trade(price_data):
        trade_executor.enter_trade()
    elif sideways_strategy.should_enter_trade(price_data):
        trade_executor.enter_trade()

    if leverage_strategy.should_exit_trade(price_data):
        trade_executor.exit_trade()
