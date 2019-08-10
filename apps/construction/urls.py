from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.construction import views

router = DefaultRouter()
router.register(r'civil', views.CivilViewSet)
router.register(r'create/civil', views.CreateCivilViewSet)
router.register(r'commission', views.CommissionViewSet)
router.register(r'create/commission', views.CreateCommissionViewSet)

urlpatterns = [
    path('api/v1/construction/', include(router.urls)),
]
