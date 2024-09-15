from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserCreateView
from .views import UserCreateView, TokenObtainPairView, UserPreferencesView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('preferences/', UserPreferencesView.as_view(), name='user-preferences'),
     path('api/cex-apis/', views.add_cex_api, name='add_cex_api'),
]
