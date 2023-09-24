from django.contrib import admin
from .models import SaleItem, Sale

class SaleIrtem(admin.ModelAdmin):
    list_display = ('sale')

    def sale_field(self, obj):
        return obj
    sale_field.short_description = 'sale'

# Registre seus modelos no Django admin
admin.site.register(SaleItem)
admin.site.register(Sale)
