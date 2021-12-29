from django.urls import path
from . import views
urlpatterns = [
    path('', views.ListViewClass.as_view(), name='listview'),
    # path('<int:id>/', views.TempDetailView.as_view(), name='tempdetail'),
]
