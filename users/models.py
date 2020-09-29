from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# custom User model refer to: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/


class User(AbstractUser):

    bio = models.TextField(default="")
