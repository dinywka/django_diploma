from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
    """
    Модель, которая содержит расширение для стандартной модели пользователя веб-платформы
    """

    user = models.OneToOneField(
        editable=True,
        blank=True,
        null=True,
        default=None,
        verbose_name="Модель пользователя",
        help_text='<small class="text-muted">Тут лежит "ссылка" на модель пользователя</small><hr><br>',
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",  # user.profile
    )
    avatar = models.ImageField(verbose_name="Аватарка", upload_to="users/avatars", default="https://vk-wiki.ru/wp-content/uploads/2019/04/male-user-profile-picture.png", null=True, blank=True)
    job_title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Должность")
    started_date = models.DateTimeField(default=now, verbose_name="Дата назначения")


    class Meta:
        """Вспомогательный класс"""

        app_label = "django_app"
        ordering = ("-user", "avatar")
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"<UserProfile {self.user.username}>"

class Ideas(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=2000)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "django_app"
        ordering = ("date_created", )
        verbose_name = "Идея по улучшению бизнеса"
        verbose_name_plural = "Идеи по улучшению бизнеса"

        def __str__(self):
            return f"<Ideas {self.Ideas.title}>"

class IdeaComments(models.Model):
    """Комментарии к идеям"""

    idea = models.ForeignKey(to=Ideas, verbose_name="К какой идее", max_length=200, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, verbose_name="Автор", max_length=200, on_delete=models.CASCADE)
    text = models.TextField("Текст комментария", default="")
    date_time = models.DateTimeField("Дата и время создания", default=now)

    class Meta:
        app_label = "django_app"
        ordering = ("-date_time", "idea")
        verbose_name = "Комментарий к посту"
        verbose_name_plural = "Комментарии к постам"

    def __str__(self):
        return f"{self.date_time} {self.author.username} {self.ideas.title} {self.text[:20]}"


class IdeaRatings(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    idea = models.ForeignKey(to=Ideas, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    class Meta:
        app_label = "django_app"
        ordering = ("-idea", "author")
        verbose_name = "Рейтинг к идее"
        verbose_name_plural = "Рейтинги к идеям"

    def __str__(self):
        if self.status:
            like = "ЛАЙК"
        else:
            like = "ДИЗЛАЙК"
        return f"{self.ideas.title} {self.author.username} {like}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_added',)

class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.IntegerField(null=True, blank=True)

class Resume(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    education = models.CharField(max_length=255)
    skills = models.TextField()
    hr_rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Рейтинг не может быть меньше 1.'),
            MaxValueValidator(10, message='Рейтинг не может быть больше 10.')
        ],
        help_text='Введите рейтинг от 1 до 10.', blank=True, default=0
    )
    hr_comment = models.CharField(max_length=500, default='no comment')
    resume_file = models.FileField(upload_to='resume_files/', null=True, blank=True)

    def update_hr_rating(self, new_rating, new_comment):
        self.hr_rating = new_rating
        self.hr_comment = new_comment
        self.save()





