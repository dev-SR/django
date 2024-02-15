from django.urls import path
from .views import StockMarketDataCreateView, StockMarketDataDeleteView, StockMarketDataListView, StockMarketDataUpdateView, StockMarketDataDetailView

urlpatterns = [
    path('', StockMarketDataListView.as_view(), name='index'),
    path('stock-market-data/create/', StockMarketDataCreateView.as_view(), name='create'),
    path('stock-market-data/<int:pk>/', StockMarketDataDetailView.as_view(), name='detail'),
    path('stock-market-data/<int:pk>/update/', StockMarketDataUpdateView.as_view(), name='update'),
    path('stock-market-data/<int:pk>/delete/', StockMarketDataDeleteView.as_view(), name='delete'),
]
