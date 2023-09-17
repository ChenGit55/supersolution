
from django.urls import path, include
from .views import sales_view, new_sale_view, SaleList, SaleViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'sales', SaleViewSet) 

urlpatterns = [
    path('', sales_view, name='sales'),
    path('new/', new_sale_view, name='new-sale'),
    path('api/', SaleList.as_view(), name='api-sales'),
    path('api/', include(router.urls)),
]