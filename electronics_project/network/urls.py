from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, ProductViewSet, EmployeeViewSet, RegisterView


router = DefaultRouter()
router.register('nodes', NetworkNodeViewSet, basename='nodes')
router.register('products', ProductViewSet, basename='products')
router.register('employees', EmployeeViewSet, basename='employees')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]
