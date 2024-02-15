from django.contrib import admin

from .models import StockMarketData


@admin.register(StockMarketData)
class StockMarketDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'trade_code',
        'high',
        'low',
        'open',
        'close',
        'volume',
    )
    list_filter = ('date',)
