# urls.py
from django.urls import path
from .views import ConversationDetailView, LandingPageView
urlpatterns = [
    path("", LandingPageView.as_view(), name="index"),
    path('conversation/<int:pk>/', ConversationDetailView.as_view(), name='conversation_detail'),
]
