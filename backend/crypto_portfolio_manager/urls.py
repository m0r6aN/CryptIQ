from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('crypto_portfolio_manager.apps.accounts.urls')),
    path('api/portfolio/', include('crypto_portfolio_manager.apps.portfolio.urls')),
    path('api/trading/', include('crypto_portfolio_manager.apps.trading.urls')),
    path('api/ai/', include('crypto_portfolio_manager.apps.ai_assistant.urls')),
    path('api/market_data/', include('crypto_portfolio_manager.apps.market_data.urls')),
]
