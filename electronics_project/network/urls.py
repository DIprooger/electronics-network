from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, ProductViewSet, EmployeeViewSet


router = DefaultRouter()
router.register('nodes', NetworkNodeViewSet)
router.register('products', ProductViewSet)
router.register('employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
