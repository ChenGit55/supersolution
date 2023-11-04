from django.contrib import admin
from .models import SaleItem, Sale

class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale','product', 'quantity', 'price', 'total']

class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'total', 'user']

admin.site.register(SaleItem, SaleItemAdmin)
admin.site.register(Sale, SaleAdmin)