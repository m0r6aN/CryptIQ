from django.test import TestCase
from apps.market_data.services import fetch_market_data, calculate_market_volatility, fetch_historical_prices

class MarketDataTests(TestCase):

    def test_fetch_market_data(self):
        data = fetch_market_data('BTCUSDT')
        self.assertIsNotNone(data)
        self.assertIn('BTCUSDT', data)

    def test_calculate_market_volatility(self):        
        historical_prices = [40000, 41000, 40500, 42000, 43000]
        volatility = calculate_market_volatility(historical_prices)
        self.assertGreater(volatility, 0)

    def test_fetch_historical_prices(self):
        prices = fetch_historical_prices('BTCUSDT', days=30)
        self.assertEqual(len(prices), 100)  # Mock returns 100 values
