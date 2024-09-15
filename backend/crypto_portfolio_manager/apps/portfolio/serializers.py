from rest_framework import serializers
from .models import (
    Portfolio, Asset, Holding, ExchangeAccount, Wallet,
    RebalancingStrategy, RebalanceSchedule
)

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class HoldingSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()

    class Meta:
        model = Holding
        fields = ['asset', 'quantity']

class PortfolioSerializer(serializers.ModelSerializer):
    holdings = HoldingSerializer(source='holding_set', many=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'holdings']

class ExchangeAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeAccount
        fields = '__all__'
        extra_kwargs = {
            'api_key': {'write_only': True},
            'api_secret': {'write_only': True}
        }

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'

class RebalancingStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = RebalancingStrategy
        fields = '__all__'

class RebalanceScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RebalanceSchedule
        fields = '__all__'
