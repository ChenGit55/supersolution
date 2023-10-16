from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
from apps.stores.models import Store
import pytz
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Sale(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def formatted_date(self):

        self.date = self.date.astimezone(pytz.timezone('America/Sao_Paulo'))
        return self.date.strftime('%d/%m/%Y - %H:%M')

    def calculate_total_sale(self):
        sale_items = self.saleitem_set.all()
        total_sale = 0.0

        for sale_item in sale_items:
            total_item = sale_item.calculate_total_item()
            sale_item.total = float(total_item)
            sale_item.save()
            total_sale += float(total_item)

        return total_sale

    def formatted_total_sale(self):
        f_total_sale = "{:,.2f}".format(self.calculate_total_sale()).replace(".",",")
        return f_total_sale

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

@receiver(pre_delete, sender=Product)
def handle_deleted_product(sender, instance, **kwargs):
    old_sales = SaleItem.objects.filter(product=instance)
    # Para cada venda antiga, você pode tomar uma ação específica
    for sale_item in old_sales:
        # Neste exemplo, você pode definir o nome do produto para "Produto excluído"
        sale_item.product.title = "Produto excluído"
        sale_item.product.save()

@receiver(pre_delete, sender=Sale)
def handle_deleted_user(sender, instance, **kwargs):
    old_sales = Sale.objects.filter(id=instance.id)
    for sale in old_sales:
        sale.user = None
        sale.save()