from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import re
from django.contrib.auth.models import User

def home(request):
    """Домашняя страница"""

    return render(request, 'django_app/home.html')

def register(request):
    """Регистрация в системе"""

    if request.method == "GET":
        return render(request, "django_app/register.html")
    elif request.method == "POST":
        email = request.POST.get("email", None)  # Admin1@gmail.com
        password = request.POST.get("password", None)  # Admin1@gmail.com
        if (
                re.match(r"[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", email) is None
        ):
            return render(
                request,
                "django_app/register.html",
                {"error": "Некорректный формат email или пароль"},
            )
        try:
            User.objects.create(
                username=email,
                password=make_password(password),
                email=email,
            )
        except Exception as error:
            return render(
                request,
                "django_app/register.html",
                {"error": str(error)},
            )
        return render(request, "django_app/home.html")
    else:
        raise ValueError("Invalid method")


def login_f(request: HttpRequest) -> HttpResponse:
    """Вход в аккаунт пользователя."""

    if request.method == "GET":
        return render(request, "blog_app/login.html")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is None:
            return render(request, "blog_app/login.html", {"error": "Некорректный email или пароль"})
        login(request, user)
        return redirect(reverse("home"))
    else:
        raise ValueError("Invalid method")


def logout_f(request: HttpRequest) -> HttpResponse:
    """Выход из аккаунта"""
    logout(request)
    return redirect(reverse('login'))

