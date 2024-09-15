from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import requests

class MarketDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch market data from an external API
        symbols = request.query_params.get('symbols', '')
        symbols_list = symbols.split(',') if symbols else []
        market_data = {}

        for symbol in symbols_list:
            # Replace with actual API call to fetch price
            response = requests.get(f'https://api.coinmarketcap.com/v1/ticker/{symbol}/')
            if response.status_code == 200:
                data = response.json()
                market_data[symbol] = {'price': float(data[0]['price_usd'])}
            else:
                market_data[symbol] = {'price': 0}

        return Response(market_data)
