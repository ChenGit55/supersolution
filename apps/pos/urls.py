from django.urls import path, include
from .views import sales_view, new_sale_view, SaleList, SaleViewSet, SaleItemList, SaleItemViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'sales', SaleViewSet) 
router.register(r'sales-items', SaleItemViewSet)

urlpatterns = [
    path('', sales_view, name='sales'),
    path('new/', new_sale_view, name='new-sale'),
    path('sales/', SaleList.as_view(), name='api-sales'),
    path('sales-items/', SaleItemList.as_view(), name='api-sales-items'),
    path('api/', include(router.urls)),
]