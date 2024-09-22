from django.urls import path
from .views import UserCreateView, add_cex_api, pin_login
from .views import UserCreateView, UserPreferencesView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', pin_login, name='pin_login'),
    path('preferences/', UserPreferencesView.as_view(), name='user-preferences'),
    path('api/cex-apis/', add_cex_api, name='add_cex_api'),
]
