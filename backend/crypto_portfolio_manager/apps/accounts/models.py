from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, pin, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is required')
        if not pin:
            raise ValueError('A 6-digit PIN is required')
        email = self.normalize_email(email)
        user = self.model(email=email, pin=pin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, pin, password=None, **extra_fields):
        user = self.create_user(email, pin, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    pin = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['pin']

    def __str__(self):
        return self.email
    
class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications_enabled = models.BooleanField(default=True)
    # Other preference fields
