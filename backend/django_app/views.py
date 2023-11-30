from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.cache import caches
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
import re
from django.contrib.auth.models import User
from . import models
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
import requests
from .serializers import ProductSerializer
from rest_framework import generics
from .tasks import generate_and_email_pdf
from django.contrib import messages

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
            return render(request, "django_app/login.html", {"error": "Некорректный email или пароль"})
        login(request, user)
        return redirect(reverse("home"))
    else:
        raise ValueError("Invalid method")
# from django.contrib.auth import authenticate, login
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import AllowAny
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_f(request):
#     if request.method == "POST":
#         username = request.data.get("username")
#         password = request.data.get("password")
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#
#             token, created = Token.objects.get_or_create(user=user)
#
#             return Response({'token': token.key, 'username': user.username})
#
#         return Response({'error': 'Логин или пароль неверные!'}, status=400)
#
#     return Response({'error': 'Метод не поддерживается!'}, status=400)

@login_required
def logout_f(request: HttpRequest) -> HttpResponse:
    """Выход из аккаунта"""
    logout(request)
    return redirect(reverse('login'))

@login_required
def profile_f(request: HttpRequest) -> HttpResponse:
    """Профиль пользователя"""
    return render(request, 'django_app/profile.html')
@login_required
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

@login_required
def ideas_list(request: HttpRequest) -> HttpResponse:
    """Отображение списка идей с пагинацией"""

    ideas = models.Ideas.objects.all()
    selected_page = request.GET.get(key="page", default=1)
    limit_post_by_page = 3
    paginator = Paginator(ideas, limit_post_by_page)
    current_page = paginator.get_page(selected_page)
    return render(request, "django_app/ideas_list.html", context={"current_page": current_page})

@login_required
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

@login_required
def idea_delete(request, pk):
    """Удаление идеи"""
    if request.method != "GET":
        raise ValueError("Invalid method")

    idea = models.Ideas.objects.get(id=int(pk))

    if idea.author != request.user:
        raise PermissionDenied("Вы не автор идеи!")

    idea.delete()
    return redirect(reverse("ideas_list"))

@login_required
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

@login_required
def idea_comment_create(request: HttpRequest, pk: str) -> HttpResponse:
    """Создание комментария."""

    idea = models.Ideas.objects.get(id=int(pk))
    text = request.POST.get("text", "")
    models.IdeaComments.objects.create(idea=idea, author=request.user, text=text)

    return redirect(reverse("idea_detail", args=(pk,)))

@login_required
def idea_rating(request: HttpRequest, pk: str, is_like: str) -> HttpResponse:
    """Рейтинг идеи"""
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

@login_required
def rooms(request):
    return render(request, "django_app/rooms.html", context={"rooms": models.Room.objects.all()})

@login_required
def create_room(request):
    if request.method == "GET":
        return render(request, "django_app/create_room.html")
    elif request.method == "POST":
        name = request.POST.get('name')
        slug = request.POST.get('slug')
    models.Room.objects.create(name=name, slug=slug)
    return redirect('rooms')

@login_required
def room(request, slug):
    room_obj = models.Room.objects.get(slug=slug)
    context = {"room": room_obj, "messages": models.Message.objects.filter(room=room_obj)[:25]}
    return render(
        request,
        "django_app/room.html",
        context=context
    )

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) '
                  'Chrome/102.0.0.0 Safari/537.36'
}

@login_required
def news(request):
    """Вывод новостей с использованием кеша"""
    cached_data = cache.get('news_data')
    if cached_data is not None:
        data2 = cached_data
    else:
        data1 = requests.get("https://fakenews.squirro.com/news/sport", headers=headers).json()
        _news = data1.get("news", [])
        data2 = [{"id": new["id"], "title": new["headline"]} for new in _news]
        cache.set('news_data', data2, timeout=3600)

    return render(request, 'django_app/news.html', {'data2': data2})

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(models.Product, pk=pk)

@login_required
def send_email(request):
    if request.method == 'POST':
        generate_and_email_pdf.delay()

    return render(request, 'django_app/home.html')

@login_required
def vacancy(request):
    """Подача и просмотр идей для улучшения бизнеса"""
    if request.method == 'GET':
        return render(request, 'django_app/vacancy.html')
    elif request.method == 'POST':
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        salary = request.POST.get('salary', None)
        models.Vacancy.objects.create(title=title, description=description, salary=salary)
        return redirect(reverse("vacancy_list"))
    else:
        raise ValueError("Invalid method")

@login_required
def vacancy_list(request: HttpRequest) -> HttpResponse:
    """Отображение списка идей с пагинацией"""

    vacancy = models.Vacancy.objects.all()
    selected_page = request.GET.get(key="page", default=1)
    limit_post_by_page = 3
    paginator = Paginator(vacancy, limit_post_by_page)
    current_page = paginator.get_page(selected_page)
    return render(request, "django_app/vacancy_list.html", context={"current_page": current_page})

@login_required
def vacancy_detail(request, pk:str):
    """Отображение детальной информации идеи"""
    vacancy = RamCache.get(f"vacancy_detail_{pk}")
    if vacancy is None:
        vacancy = models.Vacancy.objects.get(id=pk)
        RamCache.set(f"vacancy_detail_{pk}", vacancy, timeout=30)
    return render(request, "django_app/vacancy_detail.html",
                  context={"vacancy": vacancy, "is_detail_view": True})

@login_required
def vacancy_delete(request, pk):
    """Удаление идеи"""
    if request.method != "GET":
        raise ValueError("Invalid method")

    vacancy = models.Vacancy.objects.get(id=int(pk))
    vacancy.delete()
    return redirect(reverse("vacancy_list"))

@login_required
def vacancy_update(request, pk: str):
    """Обновление существующей идеи"""

    vacancy = get_object_or_404(models.Vacancy, id=int(pk))
    if request.method == "GET":
        return render(request, "django_app/vacancy_update.html", {'vacancy': vacancy})

    elif request.method == "POST":
        vacancy.title = request.POST.get("title", vacancy.title)
        vacancy.description = request.POST.get("description", vacancy.description)
        vacancy.salary = request.POST.get("salary", vacancy.salary)
        vacancy.save()
        return redirect(reverse("vacancy_list"))

    else:
        raise ValueError("Invalid method")

@login_required
def resume(request):
    if request.method == 'GET':
        return render(request, 'django_app/resume.html')
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        age = request.POST.get('age', None)
        education = request.POST.get('education', None)
        skills = request.POST.get('skills', None)
        resume_file = request.FILES.get('resume_file', None)

        new_resume = models.Resume.objects.create(name=name, age=age, education=education, skills=skills, resume_file=resume_file)

        return redirect(reverse("resume_list"))
    else:
        raise ValueError("Invalid method")

def download_resume(request, resume_id):
    resume = get_object_or_404(models.Resume, id=resume_id)

    if resume.resume_file:
        response = HttpResponse(resume.resume_file.read(), content_type='application/pdf')  # Change the content type based on your file type
        response['Content-Disposition'] = f'attachment; filename="{resume.resume_file.name}"'
        return response
    else:
        return HttpResponse("Resume file not found.", status=404)

@login_required
def resume_list(request: HttpRequest) -> HttpResponse:
    """Отображение списка идей с пагинацией"""

    resume = models.Resume.objects.all()
    selected_page = request.GET.get(key="page", default=1)
    limit_post_by_page = 3
    paginator = Paginator(resume, limit_post_by_page)
    current_page = paginator.get_page(selected_page)
    return render(request, "django_app/resume_list.html", context={"current_page": current_page})

@login_required
def add_hr_rating(request, pk):
    if request.method == 'POST':
        new_rating = request.POST.get('rating')
        new_comment = request.POST.get('comment')

        # Получаем резюме по ID
        resume = models.Resume.objects.get(id=pk)

        # Обновляем рейтинг и комментарий
        resume.update_hr_rating(new_rating, new_comment)

        messages.success(request, 'Рейтинг и комментарий успешно добавлены.')

        # Перенаправляем пользователя на страницу резюме
        return redirect('resume_detail', pk=pk)

@login_required
def resume_detail(request, pk):
    resume = RamCache.get(f"resume_detail_{pk}")
    if resume is None:
        resume = models.Resume.objects.get(id=pk)
        RamCache.set(f"resume_detail_{pk}", resume, timeout=30)

    return render(request, "django_app/resume_detail.html", context={"resume": resume, "is_detail_view": True})


def api(request):
    users = User.objects.all()
    user_list = [{'id': user.id, 'username': user.username} for user in users]
    return JsonResponse(user_list, safe=False)


class ProductListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer

@login_required
def react_page(request):
    return render(request, 'django_app/index.html')



