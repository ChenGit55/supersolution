from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField('email', unique=True)
    username = models.CharField('nome', max_length=128, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']# add additional fields in here

    def __str__(self):
        return self.email