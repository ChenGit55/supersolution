from django.db import models
from apps.products.models import Product

class Store(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
