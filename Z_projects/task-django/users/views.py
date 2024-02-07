from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import FormView


class CustomLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy("task-list")


class CustomRegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy("task-list")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("task-list")
        return super(CustomRegisterView, self).get(*args, **kwargs)
