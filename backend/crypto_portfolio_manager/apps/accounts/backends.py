from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class PinBackend(BaseBackend):
    def authenticate(self, request, pin=None):
        User = get_user_model()
        try:
            # Customize this logic based on how you're storing pins
            user = User.objects.get(pin=pin)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
