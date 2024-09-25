from data.data_fetcher import DataFetcher
from strategies import *
from backtesting.backtester import Backtester
from tasks.determine_market_conditions import DetermineMarketConditionsTask
from tasks.select_strategies import SelectStrategiesTask
from tasks.update_strategy_weights import UpdateStrategyWeightsTask
from tasks.filter_most_liquid import FilterMostLiquidTask

def main():
    token_metrics_api_key = 'YOUR_TOKEN_METRICS_API_KEY'
    data_fetcher = DataFetcher(token_metrics_api_key=token_metrics_api_key)
    data = data_fetcher.fetch_data()
    
    filter_liquid_task = FilterMostLiquidTask()
    data = filter_liquid_task.execute(data)
    
    market_conditions_task = DetermineMarketConditionsTask()
    market_conditions = market_conditions_task.execute(data)

    strategy_weights = {
        "GridRangingStrategy": 0.1,
        "TurtleTrendingStrategy": 0.1,
        "ATRStrategy": 0.1,
        "RSIDivergenceStrategy": 0.1,
        "AIEnhancedStrategy": 0.1,
        'TrendingStrategy': 0.2,
        'SidewaysStrategy': 0.2,
        'VolatilityStrategy': 0.2,
        'VolumeStrategy': 0.2,
        'BreakoutStrategy': 0.1,
        'MomentumStrategy': 0.1
    }
    
    update_weights_task = UpdateStrategyWeightsTask(strategy_weights)
    updated_weights = update_weights_task.execute(market_conditions)
    
    select_strategies_task = SelectStrategiesTask(updated_weights)
    selected_strategies = select_strategies_task.execute(market_conditions)
    
    for strategy_name in selected_strategies:
        strategy_class = globals()[strategy_name]
        strategy = strategy_class()
        backtester = Backtester(strategy, data)
        backtester.run()
        
if __name__ == "__main__":
    main()
