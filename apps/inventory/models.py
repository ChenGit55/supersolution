from django.db import models
from apps.products.models import Product
from apps.stores.models import Store


class Stock(models.Model):

    name = models.CharField(max_length=110)

    def __str__(self):
        return self.name


class Item(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, null=True, blank=True, default="Loja/Estoque, não definido")
    quantity = models.IntegerField()