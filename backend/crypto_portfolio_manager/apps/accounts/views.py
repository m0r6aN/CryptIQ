from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .models import UserPreferences, CEXAPI
from .serializers import UserPreferencesSerializer, CEXAPISerializer

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

@api_view(['POST'])
def add_cex_api(request):
    if request.method == 'POST':
        serializer = CEXAPISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'API info saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)