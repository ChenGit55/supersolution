from django.urls import path, include
from .views import sales_view, new_sale_view, add_payment_methods, sale_datail_view, exchange_view
from rest_framework import routers


urlpatterns = [
    path('', sales_view, name='sales'),
    path('new/', new_sale_view, name='new-sale'),
    path("detail/<int:sale_id>", sale_datail_view, name="sale-detail"),
    path("exchange/", exchange_view, name="exchange"),
    path('add-payment-methods', add_payment_methods, name='add-payment-methods' ),
]