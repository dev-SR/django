# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Conversation


class ConversationDetailView(LoginRequiredMixin, DetailView):
    model = Conversation
    template_name = 'chat/conversation_detail.html'
    context_object_name = 'current_conversation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch conversations where the current user is a participant
        context['conversations'] = Conversation.objects.filter(participants=self.request.user)
        return context


# views.py
class LandingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch conversations where the current user is a participant
        context['conversations'] = Conversation.objects.filter(participants=self.request.user)
        return context
