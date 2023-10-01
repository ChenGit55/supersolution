from django.contrib import admin
from .models import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'store', 'quantity']

admin.site.register(Item, ItemAdmin)
