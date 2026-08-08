from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegisterForm
from .models import Profile
from django.http import HttpResponse
from django.contrib.auth import authenticate


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
            return redirect("accounts/signup.html")

    else:
        form = RegisterForm()
    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {
                "error": "نام کاربری یا رمز عبور اشتباه است."
            }
        )

    return render(
        request,
        "accounts/login.html"
    )