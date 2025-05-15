from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import DetallePedido
import random

@receiver(pre_save, sender=DetallePedido)
def ajustar_precio_detalle(sender, instance, **kwargs):
    if not instance.pk:  # Solo para nuevos registros
        if not instance.precio_unitario:
            # Generar precio aleatorio basado en el proveedor
            instance.precio_unitario = instance.pedido.proveedor.generar_precio_aleatorio(instance.producto)
            
            # Aplicar descuento por volumen
            if instance.cantidad > 50:
                instance.precio_unitario = round(instance.precio_unitario * 0.95, 2)  # 5% de descuento