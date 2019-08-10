from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.warehouse import views

router = DefaultRouter()
router.register(r'list', views.WarehouseViewSet)
router.register(r'stocks', views.StockViewSet)
router.register(r'create/stock', views.CreateStockViewSet)
router.register(r'stock/releases', views.StockReleaseViewSet)
router.register(r'create/stocks/release', views.CreateStockReleaseViewSet)

urlpatterns = [
    path('logistics/warehouse/', views.LogisticsView.as_view(), name='logistics_directory'),
    path('api/v1/warehouse/form/stock/', views.StockFormViewSet.as_view()),
    path('api/v1/warehouse/', include(router.urls))
]
