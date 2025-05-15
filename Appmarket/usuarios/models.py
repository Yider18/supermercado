from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrador')
        EMPLEADO = 'EMPLEADO', _('Empleado')
        PROVEEDOR = 'PROVEEDOR', _('Proveedor')
    
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TipoUsuario.choices,
        default=TipoUsuario.EMPLEADO,
        verbose_name=_('Tipo de Usuario')
    )
    telefono = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        verbose_name=_('Teléfono')
    )
    direccion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('Dirección')
    )
    fecha_nacimiento = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_('Fecha de Nacimiento')
    )
    
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    
    def es_administrador(self):
        return self.tipo_usuario == self.TipoUsuario.ADMIN
    
    def es_empleado(self):
        return self.tipo_usuario == self.TipoUsuario.EMPLEADO
    
    def es_proveedor(self):
        return self.tipo_usuario == self.TipoUsuario.PROVEEDOR
# Create your models here.
