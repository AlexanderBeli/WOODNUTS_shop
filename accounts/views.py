from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm


# Create your views here.
class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserPageDetailView(generic.DetailView):
    model = get_user_model()
    template_name = "user_detail.html"


class UserUpdateView(generic.UpdateView):
    model = get_user_model()
    fields = [
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "phone_number",
        "email",
    ]
    template_name = "user_detail_update.html"
    # success_url = "user_detail.html"
