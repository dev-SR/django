from django.db import models


class StockMarketData(models.Model):
    date = models.DateField()
    trade_code = models.CharField(max_length=50)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trade_code} - {self.date}: high: {self.high}, low: {self.low}, open: {self.open}, close: {self.close}, volume: {self.volume}"
