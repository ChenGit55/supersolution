
from django.urls import path
from .views import sales_view

urlpatterns = [
    path('', sales_view, name='sales'),
]