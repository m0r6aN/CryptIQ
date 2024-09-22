from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from crypto_portfolio_manager.apps.trading.models import Trade
from crypto_portfolio_manager.apps.trading.serializers import TradeSerializer

from crypto_portfolio_manager.apps.ai_engine.sentiment_analysis import generate_ai_recommendations_for_user

from .models import (
    Portfolio, ExchangeAccount, Wallet,
    RebalancingStrategy, RebalanceSchedule
)
from .serializers import (
    PortfolioSerializer, ExchangeAccountSerializer, WalletSerializer,
    RebalancingStrategySerializer, RebalanceScheduleSerializer
)

from accounts.permissions import IsOwner

class PortfolioView(generics.RetrieveAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_object(self):
        return Portfolio.objects.get(user=self.request.user)
    
class TradeView(generics.CreateAPIView):
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # This method is called when saving the trade
        # You would call the CEX API here
        serializer.save(user=self.request.user)
    
class TradeHistoryView(generics.ListAPIView):
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user).order_by('-created_at')

class AITradeRecommendationsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Here’s where the AI magic happens!
        user = request.user
        recommendations = generate_ai_recommendations_for_user(user)
        
        return Response(recommendations, status=status.HTTP_200_OK)

class ExchangeAccountListCreateView(generics.ListCreateAPIView):
    serializer_class = ExchangeAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExchangeAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WalletListCreateView(generics.ListCreateAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RebalancingStrategyListCreateView(generics.ListCreateAPIView):
    serializer_class = RebalancingStrategySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RebalancingStrategy.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RebalancingStrategyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RebalancingStrategySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RebalancingStrategy.objects.filter(user=self.request.user)

class RebalanceScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = RebalanceScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RebalanceSchedule.objects.filter(strategy__user=self.request.user)

    def perform_create(self, serializer):
        strategy = serializer.validated_data['strategy']
        if strategy.user != self.request.user:
            raise PermissionDenied()
        serializer.save()
