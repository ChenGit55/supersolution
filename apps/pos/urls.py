
from django.urls import path
from .views import sales_view, new_sale_view

urlpatterns = [
    path('', sales_view, name='sales'),
    path('new/', new_sale_view, name='new-sale'),
]