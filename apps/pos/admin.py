from django.contrib import admin
from .models import SaleItem, Sale, PaymentMethod, Payment

class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale','product', 'quantity', 'price', 'total']

class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'total', 'user']

admin.site.register(SaleItem, SaleItemAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Payment)