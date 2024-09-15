from django.db import models
from django.conf import settings

class Trade(models.Model):
    TRADE_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('SWAP', 'Swap'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    asset = models.ForeignKey('portfolio.Asset', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_type} {self.quantity} {self.asset.symbol} by {self.user.email}"
