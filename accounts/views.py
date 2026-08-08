from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegisterForm
from .models import Profile
from django.http import HttpResponse


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            Profile.objects.create(user=user)
            login(request, user)
            return redirect("/")

    else:
        form = RegisterForm()
    return Httpresponse("hello")