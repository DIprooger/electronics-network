import qrcode
from io import BytesIO
from celery import shared_task
from .models import NetworkNode
from decimal import Decimal
import random
from django.core.mail import EmailMessage

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

@shared_task
def send_qr_email(node_id, recipient_email):
    try:
        node = NetworkNode.objects.select_related('address').get(id=node_id)
        contact_info = (
            f"Name: {node.name}\n"
            f"Email: {node.email}\n"
            f"Address: {node.address.country}, {node.address.city}, "
            f"{node.address.street}, {node.address.house_number}"
        )
        qr_img = qrcode.make(contact_info)
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)

        email = EmailMessage(
            subject='QR-код с контактами',
            body='Во вложении QR-код с контактной информацией узла сети.',
            from_email=None,
            to=[recipient_email],
        )
        email.attach('contact_qr.png', buffer.getvalue(), 'image/png')
        email.send()
        return f"Email отправлен {recipient_email}"

    except NetworkNode.DoesNotExist:
        return f"Узел с ID {node_id} не найден"
