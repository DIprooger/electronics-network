from django.contrib import admin
from .models import Address, NetworkNode, Product, Employee
from .tasks import async_clear_debt
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter

@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    if queryset.count() > 20:
        async_clear_debt.delay(list(queryset.values_list('id', flat=True)))
        modeladmin.message_user(request, 'Задача запущена асинхронно')
    else:
        for obj in queryset:
            obj.debt_to_supplier = 0
            obj.save()

class CityFilter(SimpleListFilter):
    title = 'Город'
    parameter_name = 'city'

    def lookups(self, request, model_admin):
        cities = Address.objects.values_list('city', flat=True).distinct()
        return [(city, city) for city in cities]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(address__city=self.value())
        return queryset

@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'email', 'supplier_link', 'debt_to_supplier', 'hierarchy_level', 'created_at')
    list_filter = (CityFilter,)
    search_fields = ('name', 'address__city', 'email')
    actions = [clear_debt]

    def city(self, obj):
        return obj.address.city

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html("<a href='/admin/network/networknode/{}/change/'>{}</a>",
                   obj.supplier.id,
                   obj.supplier.name)
        return "--"

    supplier_link.short_description = "Supplier"
    supplier_link.admin_order_field = 'supplier__name'

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'market_launch_date', 'get_nodes')

    def get_nodes(self, obj):
        return ", ".join([node.name for node in obj.node.all()])
    get_nodes.short_description = 'Узлы'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'node')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'street', 'house_number')
