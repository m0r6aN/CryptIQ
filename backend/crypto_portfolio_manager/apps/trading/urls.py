from django.urls import path
from .views import TradeListCreateView

urlpatterns = [
    path('', TradeListCreateView.as_view(), name='trade-list-create'),
]
