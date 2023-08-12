from django.urls import path
from .views import clients_list_view

urlpatterns = [
    path('', clients_list_view, name='clients')
]