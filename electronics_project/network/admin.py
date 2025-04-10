from django.contrib import admin
from .models import Address, NetworkNode, Product, Employee

@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    for obj in queryset:
        obj.debt_to_supplier = 0
        obj.save()

@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'email', 'supplier_link', 'debt_to_supplier', 'hierarchy_level', 'created_at')
    list_filter = ('address__city',)
    search_fields = ('name', 'address__city', 'email')
    action = [clear_debt]

    def city(self, obj):
        return obj.address.city

    def supplier_link(self, obj):
        if obj.supplier:
            return f"<a href='/admin/network/networknode/{obj.supplier.id}/change/'>{obj.supplier.name}</a>"
        return "--"

    supplier_link.allow_tags = True
    supplier_link.short_description = "Supplier"
    supplier_link.admin_order_field = 'supplier__name'

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'market_launch_date', 'node')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'node')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street', 'house_number')
