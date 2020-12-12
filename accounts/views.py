from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView, TemplateView
from . import forms
from .models import User


DEFAULT = 'default.png'
# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/view_profile.html', args)

class ProfileUpdate(UpdateView):
    fields = ("username","email")
    model = User
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:view_profile")

class PictureUpdate(UpdateView):
    fields = ['avatar']
    model = User
    template_name = "accounts/change_profile.html"
    success_url = reverse_lazy("accounts:view_profile")
