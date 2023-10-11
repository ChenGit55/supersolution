from django.contrib import admin
from django.urls import path, include
from .views import home_view, manage_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage/', manage_view, name="manage"),
    path('', home_view, name="home"),
    path('accounts/', include('apps.accounts.urls')),
    path('products/', include('apps.products.urls')),
    path('pos/', include('apps.pos.urls')),
    path('clients/', include('apps.clients.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('stores/', include('apps.stores.urls')),
]