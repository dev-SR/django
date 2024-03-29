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

    def dispatch(self, request, *args, **kwargs):
        """ The dispatch method in Django views is responsible for handling incoming requests and routing them to the appropriate handler method. It's often used for permission checking, pre-processing, and error handling before executing the main handler method (e.g., get, post). """
        # Get the conversation object
        self.object = self.get_object()

        # Check if the user is a participant in the conversation
        if not self.object.participants.filter(pk=request.user.pk).exists():
            # If user is not a participant, return a 404 response
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

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
