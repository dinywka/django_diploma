from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)



