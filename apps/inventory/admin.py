from django.contrib import admin
from .models import Item, Stock

class ItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity']

admin.site.register(Item, ItemAdmin)
admin.site.register(Stock)