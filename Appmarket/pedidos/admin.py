from django.contrib import admin
from .models import Proveedor, Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1
    readonly_fields = ['subtotal']

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'proveedor', 'fecha_pedido', 'estado', 'total']
    list_filter = ['estado', 'proveedor']
    search_fields = ['id', 'proveedor__nombre']
    inlines = [DetallePedidoInline]
    readonly_fields = ['fecha_pedido', 'creado_por', 'total']
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'contacto', 'telefono', 'email', 'rating', 'activo']
    search_fields = ['nombre', 'contacto', 'email']
    list_filter = ['activo']

admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Pedido, PedidoAdmin)

