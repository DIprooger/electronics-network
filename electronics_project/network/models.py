from django.db import models

class Address(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"

class NetworkNode(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='network_node')

    supplier = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subnodes')

    debt_to_supplier = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.supplier}"

    @property
    def hierarchy_level(self):
        level = 0
        current = self.supplier
        while current is not None:
            level += 1
            current = current.supplier
        return level

class Product(models.Model):
    node = models.ManyToManyField(NetworkNode, related_name='products')
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=150)
    market_launch_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.model})"

class Employee(models.Model):
    node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name='employees')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.full_name
