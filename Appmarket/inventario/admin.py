from django.contrib import admin
from .models import Producto, Categoria

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'cantidad', 'stock_minimo', 'estado')
    list_filter = ('categoria', 'estado')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'cantidad', 'stock_minimo')
    readonly_fields = ('creado_por', 'fecha_creacion', 'fecha_actualizacion')
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre', 'descripcion')

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
# Register your models here.
