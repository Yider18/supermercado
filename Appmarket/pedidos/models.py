from django.db import models
from django.utils.translation import gettext_lazy as _
from usuarios.models import Usuario
from inventario.models import Producto
import random
from datetime import timedelta

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, verbose_name=_('Nombre'))
    contacto = models.CharField(max_length=100, verbose_name=_('Persona de Contacto'))
    telefono = models.CharField(max_length=15, verbose_name=_('Teléfono'))
    email = models.EmailField(verbose_name=_('Email'))
    direccion = models.TextField(verbose_name=_('Dirección'))
    rating = models.FloatField(default=3.0, verbose_name=_('Rating (1-5)'))
    tiempo_respuesta_promedio = models.IntegerField(default=3, verbose_name=_('Tiempo Respuesta (días)'))
    activo = models.BooleanField(default=True, verbose_name=_('Activo'))
    
    class Meta:
        verbose_name = _('Proveedor')
        verbose_name_plural = _('Proveedores')
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} (Rating: {self.rating}/5)"
    
    def generar_precio_aleatorio(self, producto):
        """Genera un precio aleatorio basado en el precio base del producto"""
        variacion = random.uniform(0.85, 1.15)  # ±15% de variación
        return round(producto.precio * variacion, 2)

class Pedido(models.Model):
    class EstadoPedido(models.TextChoices):
        PENDIENTE = 'PENDIENTE', _('Pendiente')
        APROBADO = 'APROBADO', _('Aprobado')
        RECHAZADO = 'RECHAZADO', _('Rechazado')
        ENVIADO = 'ENVIADO', _('Enviado')
        RECIBIDO = 'RECIBIDO', _('Recibido')
        CANCELADO = 'CANCELADO', _('Cancelado')
    
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='pedidos',
        verbose_name=_('Proveedor')
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de Pedido'))
    fecha_entrega_estimada = models.DateField(verbose_name=_('Fecha Entrega Estimada'))
    fecha_recepcion = models.DateField(
        blank=True, 
        null=True,
        verbose_name=_('Fecha de Recepción'))
    estado = models.CharField(
        max_length=10,
        choices=EstadoPedido.choices,
        default=EstadoPedido.PENDIENTE,
        verbose_name=_('Estado'))
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='pedidos_creados',
        verbose_name=_('Creado por'))
    notas = models.TextField(blank=True, null=True, verbose_name=_('Notas'))
    
    class Meta:
        verbose_name = _('Pedido')
        verbose_name_plural = _('Pedidos')
        ordering = ['-fecha_pedido']
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.proveedor.nombre}"
    
    @property
    def total(self):
        return sum(detalle.subtotal for detalle in self.detalles.all())
    
    def puede_aprobar(self):
        return self.estado == self.EstadoPedido.PENDIENTE
    
    def puede_recibir(self):
        return self.estado == self.EstadoPedido.ENVIADO
    
    def tiempo_espera(self):
        if self.fecha_recepcion:
            return (self.fecha_recepcion - self.fecha_pedido.date()).days
        return (self.fecha_entrega_estimada - self.fecha_pedido.date()).days

class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name=_('Pedido'))
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        verbose_name=_('Producto'))
    cantidad = models.PositiveIntegerField(verbose_name=_('Cantidad'))
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Precio Unitario'))
    
    class Meta:
        verbose_name = _('Detalle de Pedido')
        verbose_name_plural = _('Detalles de Pedido')
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - ${self.precio_unitario}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
