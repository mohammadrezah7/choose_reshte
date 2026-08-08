
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError

from .forms import RegisterForm
from .models import Profile


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )

                Profile.objects.create(user=user)

            except IntegrityError:
                form.add_error(
                    "username",
                    "این نام کاربری قبلاً ثبت شده است. لطفاً نام کاربری دیگری انتخاب کنید."
                )

                return render(
                    request,
                    "accounts/signup.html",
                    {"form": form}
                )

            login(request, user)

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/signup.html",
        {"form": form}
    )


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

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

