from django import forms
from .models import Pedido, DetallePedido, Proveedor
from inventario.models import Producto

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion', 'rating', 'tiempo_respuesta_promedio', 'activo']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['proveedor', 'fecha_entrega_estimada', 'notas']
        widgets = {
            'fecha_entrega_estimada': forms.DateInput(attrs={'type': 'date'}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad', 'precio_unitario']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(estado='ACTIVO')