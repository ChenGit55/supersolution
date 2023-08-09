
from django.urls import path
from .views import product_list_view, new_product_view

urlpatterns = [
    path('', product_list_view, name="home"),
    path('new/', new_product_view, name="new-product")
]