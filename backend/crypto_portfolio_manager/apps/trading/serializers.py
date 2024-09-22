from rest_framework import serializers
from .models import Trade
from crypto_portfolio_manager.apps.portfolio.serializers import AssetSerializer

class TradeSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()

    class Meta:
        model = Trade
        fields = ['id', 'user', 'trade_type', 'asset', 'quantity', 'price', 'timestamp']
