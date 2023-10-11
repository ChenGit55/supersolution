from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.stores.models import Store

class CustomUser(AbstractUser):

    SELLER = 'Vendedor'
    STOCKIST = 'Estoquista'
    ADMINISTRATOR = 'Administrador'
    SUPORT = 'Suport'

    ACESS_CHOICES = [
        (SELLER, 'Vendedor'),
        (STOCKIST, 'Estoquista'),
        (ADMINISTRATOR, 'Administrador'),
        (SUPORT, 'Suporte'),
    ]
    
    username = models.CharField('nome', max_length=128, unique=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, default=None)
    acess_level = models.CharField(max_length=15, choices=ACESS_CHOICES, default=SELLER)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    def __str__(self):
        return self.username