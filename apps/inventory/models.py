from django.db import models
from apps.products.models import Product
from apps.stores.models import Store





class Stock(models.Model):

    name = models.CharField(max_length=110)

    def __str__(self):
        return self.name


class Location(models.Model):

    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)


class Item(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
