from rest_framework import serializers
from .models import  Address, NetworkNode, Product, Employee
from django.contrib.auth.models import User
from datetime import date

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validate_data):
        user = User.objects.create_user(**validate_data)
        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=25)
    class Meta:
        model = Product
        fields = '__all__'

    def validate_market_launch_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Дата выхода не может быть прошедшего число")
        return value

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class NetworkNodeSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    products = ProductSerializer(many=True, read_only=True)
    employees = EmployeeSerializer(many=True, read_only=True)
    hierarchy_level = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    class Meta:
        model = NetworkNode
        exclude = ['debt_to_supplier']

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()

        return instance