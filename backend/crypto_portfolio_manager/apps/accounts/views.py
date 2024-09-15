from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from .models import UserPreferences
from .serializers import UserPreferencesSerializer

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class UserPreferencesView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserPreferences.objects.get(user=self.request.user)
