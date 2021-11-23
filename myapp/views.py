from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Talk

User = get_user_model()


class IndexView(generic.TemplateView):
    template_name = "index.html"
    


class FriendsView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "friends.html"