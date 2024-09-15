from django.urls import path
from .views import (
    PortfolioView, ExchangeAccountListCreateView, WalletListCreateView,
    RebalancingStrategyListCreateView, RebalancingStrategyDetailView,
    RebalanceScheduleListCreateView
)

urlpatterns = [
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('exchange-accounts/', ExchangeAccountListCreateView.as_view(), name='exchange-accounts'),
    path('wallets/', WalletListCreateView.as_view(), name='wallets'),
    path('strategies/', RebalancingStrategyListCreateView.as_view(), name='strategies'),
    path('strategies/<int:pk>/', RebalancingStrategyDetailView.as_view(), name='strategy-detail'),
    path('schedules/', RebalanceScheduleListCreateView.as_view(), name='schedules'),
]
