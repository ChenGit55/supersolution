from django.urls import path
from .views import store_view, create_store_view

urlpatterns = [
    path('', store_view, name="stores"),
    path('creation/', create_store_view, name="store-creation" ),
]