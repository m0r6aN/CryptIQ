from trading.exchange_api import ExchangeAPI
from utils.risk_management import RiskManagement

class Trader:
    def __init__(self, api_key, secret):
        self.exchange_api = ExchangeAPI(api_key, secret)
        self.risk_management = RiskManagement()

    def execute_trade(self, symbol, side, amount, leverage):
        self.exchange_api.set_leverage(symbol, leverage)
        self.exchange_api.create_order(symbol, side, amount)