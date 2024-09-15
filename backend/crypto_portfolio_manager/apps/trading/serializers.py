from rest_framework import serializers
from .models import Trade
from portfolio.serializers import AssetSerializer

class TradeSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()

    class Meta:
        model = Trade
        fields = ['id', 'user', 'trade_type', 'asset', 'quantity', 'price', 'timestamp']
