from django.shortcuts import render
from django.db.models import Avg
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import NetworkNode, Product, Employee, Address
from .serializers import NetworkNodeSerializer, ProductSerializer, EmployeeSerializer, RegisterSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from .tasks import send_qr_email


@extend_schema(request=RegisterSerializer, responses={201: {'token': '111111111'}})
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IsActiveUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.none()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['address__country']

    def get_queryset(self):
        return NetworkNode.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        request.data.pop('debt_to_supplier', None)
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def above_average_debt(self, request):
        avg_debt = NetworkNode.objects.aggregate(avg=Avg('debt_to_supplier'))['avg']
        queryset = NetworkNode.objects.filter(debt_to_supplier__gt=avg_debt)
        serializer = self.get_serializer(queryset, many=True)

        enriched_data = []
        for obj, serializer in zip(queryset, serializer.data):
            enriched = dict(serializer)
            enriched['debt_to_supplier'] = float(obj.debt_to_supplier)
            enriched_data.append(enriched)
        return Response({
            'average_debt': round(avg_debt, 2),
            'count': queryset.count(),
            'nodes': enriched_data
        })

    @extend_schema(parameters=[OpenApiParameter(name='product_id', type=int, required=True, description='ID продукта')])
    @action(detail=False, methods=['get'])
    def by_product(self, request):
        product_id = request.query_params.get('product_id')
        queryset = NetworkNode.objects.filter(products__id=product_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_qr(self, request, pk=None):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        send_qr_email.delay(pk, email)
        return Response({'status': 'Задача на отправку QR-кода запущена'})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.none()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        return Product.objects.filter(node__owner=self.request.user)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.none()
    serializer_class = EmployeeSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        return Employee.objects.filter(node__owner=self.request.user)
