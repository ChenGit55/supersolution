from django.urls import path
from .views import inventory_view, add_product_view

urlpatterns = [
    path('', inventory_view, name="inventory"),
    path('add-product', add_product_view, name="add-product"),
]