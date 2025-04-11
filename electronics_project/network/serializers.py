from rest_framework import serializers
from .models import  Address, NetworkNode, Product, Employee

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class NetworkNodeSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    products = ProductSerializer(many=True, read_only=True)
    employees = EmployeeSerializer(many=True, read_only=True)
    hierarchy_level = serializers.IntegerField(read_only=True)
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