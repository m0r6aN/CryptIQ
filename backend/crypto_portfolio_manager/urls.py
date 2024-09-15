from django.contrib import admin
from django.urls import path, include
from .views import MarketDataView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('crypto_portfolio_manager.apps.accounts.urls')),
    path('api/portfolio/', include('crypto_portfolio_manager.apps.portfolio.urls')),
    path('api/trading/', include('crypto_portfolio_manager.apps.trading.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('market-data/', MarketDataView.as_view(), name='market-data'),
]
