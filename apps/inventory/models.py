from django.db import models
from apps.products.models import Product
from apps.stores.models import Store



class Item(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.product} - Quantidade: {self.quantity} - Loja: {self.store}'