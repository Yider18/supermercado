from django.core.management.base import BaseCommand
from pedidos.models import Proveedor
from faker import Faker
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = 'Popula la base de datos con proveedores de prueba'

    def handle(self, *args, **kwargs):
        nombres_proveedores = [
            "Distribuciones Alimenticias S.A.",
            "Mayorista de Alimentos Unidos",
            "Proveedora de Víveres Nacional",
            "Suministros Rápidos",
            "Alimentos Frescos Ltda.",
            "Distribuidora Comercial del Valle",
            "Importadora de Alimentos S.A.",
            "Productos Selectos del Campo",
            "Comercializadora Internacional",
            "Distribuidora Mayorista Andina"
        ]

        for nombre in nombres_proveedores:
            # Crear proveedor con datos aleatorios
            Proveedor.objects.create(
                nombre=nombre,
                contacto=fake.name(),
                telefono=fake.phone_number(),
                email=fake.company_email(),
                direccion=fake.address(),
                rating=round(random.uniform(2.5, 5.0), 1),
                tiempo_respuesta_promedio=random.randint(1, 7),
                activo=random.choice([True, True, True, False])  # 75% de probabilidad de estar activo
            )

        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(nombres_proveedores)} proveedores de prueba'))