from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
from apps.stores.models import Store
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Sale(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_DEFAULT, default=None)
    date = models.DateTimeField(verbose_name="data", max_length=8, default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    serial = models.TextField(null=True, blank=True)
    observation = models.TextField(null=True, blank=True)

    def calculate_total_sale(self):
        sale_items = self.saleitem_set.all()
        total_sale = 0.0

        for sale_item in sale_items:
            total_item = sale_item.calculate_total_item()
            sale_item.total = float(total_item)
            sale_item.save()
            total_sale += float(total_item)

        return total_sale

    def save(self, *args, **kwargs):
        self.total = self.calculate_total_sale()
        super().save(*args, **kwargs)

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def calculate_total_item(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        self.total = self.calculate_total_item()
        super().save(*args, **kwargs)


class Payment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    change = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.method} - {self.value}'
    
class DailyReport:
    initial = models.PositiveIntegerField()
    final = models.PositiveIntegerField()
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(verbose_name="data", max_length=8, default=timezone.now)


@receiver(pre_delete, sender=Product)
def handle_deleted_product(sender, instance, **kwargs):
    old_sales = SaleItem.objects.filter(product=instance)
    for sale_item in old_sales:
        sale_item.product.title = "Produto excluído"
        sale_item.product.save()

@receiver(pre_delete, sender=Sale)
def handle_deleted_user(sender, instance, **kwargs):
    old_sales = Sale.objects.filter(id=instance.id)
    for sale in old_sales:
        sale.user = None
        sale.save()