from django.db import models
from apps.products.models import Product

class Store(models.Model):
    name = models.CharField(max_length=50)

class Stock(models.Model):
    name = models.CharField(max_length=50)

class ProducStock(models.Model):
    quantity = models.PositiveIntegerField()