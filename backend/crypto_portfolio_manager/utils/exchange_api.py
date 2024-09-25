import ccxt

class ExchangeAPI:
    def __init__(self, api_key, secret, exchange_name='binance'):
        self.exchange = getattr(ccxt, exchange_name)({
            'apiKey': api_key,
            'secret': secret,
        })

    def create_order(self, symbol, side, amount, price=None, params={}):
        return self.exchange.create_order(symbol, 'market', side, amount, price, params)

    def set_leverage(self, symbol, leverage):
        self.exchange.fapiPrivate_post_leverage({'symbol': symbol.replace('/', ''), 'leverage': leverage})