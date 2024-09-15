from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ExchangeAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange_name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Asset(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assets = models.ManyToManyField(Asset, through='Holding')
    created_at = models.DateTimeField(auto_now_add=True)

class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    updated_at = models.DateTimeField(auto_now=True)

class RebalancingStrategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_allocations = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class RebalanceSchedule(models.Model):
    strategy = models.ForeignKey(RebalancingStrategy, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=50)
    next_run = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
