from django.shortcuts import render
from django.db.models import Avg
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import NetworkNode, Product, Employee
from .serializers import NetworkNodeSerializer, ProductSerializer, EmployeeSerializer

class IsActiveUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['address__country']

    def update(self, request, *args, **kwargs):
        request.data.pop('debt_to_supplier', None)
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def above_average_debt(self, request):
        avg_debt = NetworkNode.objects.aggregate(avg=Avg('debt_to_supplier'))['avg']
        queryset = NetworkNode.objects.filter(debt_to_supplier__gt=avg_debt)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_product(self, request):
        product_id = request.query_params.get('product_id')
        queryset = NetworkNode.objects.filter(products__id=product_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveUser]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsActiveUser]
