from celery import shared_task
from .models import NetworkNode
from decimal import Decimal
import random

@shared_task
def async_clear_debt(node_ids):
    for node_id in node_ids:
        node = NetworkNode.objects.get(id=node_id)
        node.debt_to_supplier = 0
        node.save()

@shared_task
def increase_debt():
    nodes = NetworkNode.objects.all()
    for node in nodes:
        increase = Decimal(random.uniform(5, 500)).quantize(Decimal("0.01"))
        node.debt_to_supplier += increase
        node.save()
    return f"Увеличено случайно всем узлам на сумму от 5 до 500"

@shared_task
def decrease_debt():
    nodes = NetworkNode.objects.all()
    for node in nodes:
        decrease = Decimal(random.uniform(100, 10000)).quantize(Decimal("0.01"))
        node.debt_to_supplier = max(0, node.debt_to_supplier - decrease)
        node.save()
    return f"Уменьшено случайно всем узлам на сумму от 100 до 10000"
