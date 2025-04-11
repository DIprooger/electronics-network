from django.core.management.base import BaseCommand
from network.models import Address, NetworkNode, Product, Employee
from faker import Faker
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Автоматически заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        fake = Faker('ru_RU')
        nodes = []

        for i in range(2):
            addr = Address.objects.create(
                country=fake.country(),
                city=fake.city(),
                street=fake.street_name(),
                house_number=fake.building_number()
            )
            node = NetworkNode.objects.create(
                name=f"Завод {fake.company()}",
                email=fake.company_email(),
                address=addr,
                supplier=None,
                debt_to_supplier=0
            )
            nodes.append(node)

        for level in range(1, 5):
            for _ in range(3):
                addr = Address.objects.create(
                    country=fake.country(),
                    city=fake.city(),
                    street=fake.street_name(),
                    house_number=fake.building_number()
                )
                supplier = random.choice(nodes)
                node = NetworkNode.objects.create(
                    name=fake.company(),
                    email=fake.company_email(),
                    address=addr,
                    supplier=supplier,
                    debt_to_supplier=round(random.uniform(1000, 50000), 2)
                )
                nodes.append(node)

        for node in nodes:
            for _ in range(random.randint(1, 3)):
                Product.objects.create(
                    node=node,
                    name=fake.word().capitalize(),
                    model=f"Model-{random.randint(100,999)}",
                    market_launch_date=date.today() - timedelta(days=random.randint(30, 1000))
                )

        for node in nodes:
            for _ in range(random.randint(1, 4)):
                Employee.objects.create(
                    node=node,
                    full_name=fake.name(),
                    email=fake.email()
                )

        self.stdout.write(self.style.SUCCESS(f'✔ Успешно создано {len(nodes)} узлов сети, с продуктами и сотрудниками.'))
