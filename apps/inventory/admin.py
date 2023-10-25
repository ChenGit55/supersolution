from django.contrib import admin
from .models import Item, Stock

class ItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'location']

admin.site.register(Item, ItemAdmin)
admin.site.register(Stock)