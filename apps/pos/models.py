from django.db import models
from apps.accounts.models import CustomUser
from apps.products.models import Product
from decimal import Decimal
import locale

class Sale(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.formatted_date()} - {self.user.username}'
    
    def formatted_date(self):
        return self.date.strftime('%d/%m/%Y - %H:%M')
    
    def calculate_total_sale(self):
        sale_items = self.saleitem_set.all()
        total_sale = Decimal('0.00')

        for sale_item in sale_items:
            total_item = sale_item.calculate_total_item()
            sale_item.total = total_item
            sale_item.save()
            total_sale += Decimal(total_item)

        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        formatted_total_sale = locale.currency(total_sale, grouping=True, symbol='')
        locale.setlocale(locale.LC_ALL, '')

        return formatted_total_sale.rjust(10)
    
  

    def save(self, *args, **kwargs):
        self.total = self.calculate_total_sale()
        super().save(*args, **kwargs) 

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f' ({self.sale.id}) - Name: {self.product} - Qtd: {self.quantity} - Price: {self.price} - Total: {self.total}'

    def calculate_total_item(self):
        return self.quantity * self.price
    
    def save(self, *args, **kwargs):
        self.total = self.calculate_total_item()
        super().save(*args, **kwargs)