from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.stores.models import Store

class CustomUser(AbstractUser):
    username = models.CharField('nome', max_length=128, unique=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, default='', null=True, blank=True)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username