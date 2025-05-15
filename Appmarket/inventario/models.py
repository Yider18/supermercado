from django.db import models 
from django.utils.translation import gettext_lazy as _
from usuarios.models import Usuario
from django.db import models
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name=_('Nombre'))
    descripcion = models.TextField(blank=True, null=True, verbose_name=_('Descripción'))
    
    class Meta:
        verbose_name = _('Categoría')
        verbose_name_plural = _('Categorías')
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    class EstadoProducto(models.TextChoices):
        ACTIVO = 'ACTIVO', _('Activo')
        INACTIVO = 'INACTIVO', _('Inactivo')
        DESCONTINUADO = 'DESCONTINUADO', _('Descontinuado')
    
    nombre = models.CharField(max_length=100, verbose_name=_('Nombre'))
    descripcion = models.TextField(blank=True, null=True, verbose_name=_('Descripción'))
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_('Categoría')
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name=_('Precio Unitario')
    )
    cantidad = models.IntegerField(default=0, verbose_name=_('Cantidad en Stock'))
    stock_minimo = models.IntegerField(default=5, verbose_name=_('Stock Mínimo'))
    fecha_vencimiento = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_('Fecha de Vencimiento')
    )
    estado = models.CharField(
        max_length=15,
        choices=EstadoProducto.choices,
        default=EstadoProducto.ACTIVO,
        verbose_name=_('Estado')
    )
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='productos_creados',
        verbose_name=_('Creado por')
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de Creación'))
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name=_('Fecha de Actualización'))
    
    class Meta:
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} (Stock: {self.cantidad})"
    
    def necesita_reabastecimiento(self):
        return self.cantidad <= self.stock_minimo
    
    def proximo_a_vencer(self):
        from datetime import date, timedelta
        return self.fecha_vencimiento and self.fecha_vencimiento <= date.today() + timedelta(days=30)