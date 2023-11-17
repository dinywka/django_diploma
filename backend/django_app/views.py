from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import re
from django.contrib.auth.models import User
from . import models

RamCache = caches["default"]

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
        return render(request, "django_app/login.html")
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

def profile_f(request: HttpRequest) -> HttpResponse:
    """Профиль пользователя"""
    return render(request, 'django_app/profile.html')

def ideas(request):
    """Подача и просмотр идей для улучшения бизнеса"""
    if request.method == 'GET':
        return render(request, 'django_app/ideas.html')
    elif request.method == 'POST':
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        models.Ideas.objects.create(title=title, description=description, author=request.user, date_created=datetime.now)
        return redirect(reverse("ideas_list"))
    else:
        raise ValueError("Invalid method")

def ideas_list(request: HttpRequest) -> HttpResponse:
    """Отображение списка идей с пагинацией"""

    ideas = models.Ideas.objects.all()
    selected_page = request.GET.get(key="page", default=1)
    limit_post_by_page = 3
    paginator = Paginator(ideas, limit_post_by_page)
    current_page = paginator.get_page(selected_page)
    return render(request, "django_app/ideas_list.html", context={"current_page": current_page})

def idea_detail(request, pk:str):
    """Отображение детальной информации идеи"""
    idea = RamCache.get(f"idea_detail_{pk}")
    if idea is None:
        idea = models.Ideas.objects.get(id=pk)
        RamCache.set(f"idea_detail_{pk}", idea, timeout=30)

    comments = models.IdeaComments.objects.filter(idea=idea)
    ratings = models.IdeaRatings.objects.filter(idea=idea)
    ratings = {
        "like": ratings.filter(status=True).count(),
        "dislike": ratings.filter(status=False).count(),
        "total": ratings.filter(status=True).count() - ratings.filter(status=False).count(),
    }

    return render(request, "django_app/idea_detail.html",
                  context={"idea": idea, "comments": comments, "ratings": ratings, "is_detail_view": True})

def idea_delete(request, pk):
    """Удаление идеи"""
    if request.method != "GET":
        raise ValueError("Invalid method")

    idea = models.Ideas.objects.get(id=int(pk))

    if idea.author != request.user:
        raise PermissionDenied("Вы не автор идеи!")

    idea.delete()
    return redirect(reverse("ideas_list"))


def idea_update(request, pk: str):
    """Обновление существующей идеи"""

    idea = get_object_or_404(models.Ideas, id=int(pk))
    if idea.author != request.user:
        raise PermissionDenied("Вы не автор идеи!")
    else:
        if request.method == "GET":
            return render(request, "django_app/idea_update.html", {'idea': idea})

        elif request.method == "POST":
            idea.title = request.POST.get("title", idea.title)
            idea.description = request.POST.get("description", idea.description)

            idea.save()
            return redirect(reverse("ideas_list"))

        else:
            raise ValueError("Invalid method")

def idea_comment_create(request: HttpRequest, pk: str) -> HttpResponse:
    """Создание комментария."""

    idea = models.Ideas.objects.get(id=int(pk))
    text = request.POST.get("text", "")
    models.IdeaComments.objects.create(idea=idea, author=request.user, text=text)

    return redirect(reverse("idea_detail", args=(pk,)))

def idea_rating(request: HttpRequest, pk: str, is_like: str) -> HttpResponse:
    idea = models.Ideas.objects.get(id=int(pk))
    is_like = True if str(is_like).lower().strip() == "лайк" else False

    ratings = models.IdeaRatings.objects.filter(idea=idea, author=request.user)
    if len(ratings) < 1:
        models.IdeaRatings.objects.create(idea=idea, author=request.user, status=is_like)
    else:
        rating = ratings[0]
        if is_like == True and rating.status == True:
            rating.delete()
        elif is_like == False and rating.status == False:
            rating.delete()
        else:
            rating.status = is_like
            rating.save()

    return redirect(reverse("idea_detail", args=(pk,)))