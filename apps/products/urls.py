from django.urls import path
from .views import product_list_view, new_product_view, product_detail_view

urlpatterns = [
    path('', product_list_view, name="products"),
    path('new/', new_product_view, name="new-product"),
    path('detail/<str:code>', product_detail_view, name="product-detail"),
]