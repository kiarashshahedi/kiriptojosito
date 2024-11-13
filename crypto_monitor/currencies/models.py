from django.db import models

class CurrencyChange(models.Model):
    symbol = models.CharField(max_length=20)
    price_change_percent = models.FloatField()
    last_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.price_change_percent}%"
