from django.db.models import Q, F, Subquery, OuterRef, Avg
from django.db import models
from datetime import date, timedelta
from pedidos.models import Proveedor, DetallePedido
import random

class OptimizadorPedidos:
    @staticmethod
    def generar_sugerencias():
        sugerencias = []
        productos = Producto.objects.filter(
            Q(cantidad__lte=F('stock_minimo')) |
            Q(fecha_vencimiento__lte=date.today() + timedelta(days=30)),
            estado='ACTIVO'
        ).distinct()
        
        for producto in productos:
            proveedores_con_historial = Proveedor.objects.filter(
                detalles_pedidos__producto=producto
            ).annotate(
                ultimo_precio=Subquery(
                    DetallePedido.objects.filter(
                        producto=producto,
                        pedido__proveedor=OuterRef('pk')
                    ).order_by('-pedido__fecha_pedido').values('precio_unitario')[:1]
                ),
                tiempo_entrega_avg=Avg('pedidos__fecha_recepcion - pedidos__fecha_pedido')
            ).exclude(ultimo_precio__isnull=True)
            
            proveedores_sin_historial = Proveedor.objects.exclude(
                id__in=proveedores_con_historial.values('id')
            )
            
            todos_proveedores = list(proveedores_con_historial)
            
            for proveedor in proveedores_sin_historial:
                proveedor.ultimo_precio = proveedor.generar_precio_aleatorio(producto)
                proveedor.tiempo_entrega_avg = timedelta(
                    days=proveedor.tiempo_respuesta_promedio + random.randint(-1, 1)
                )
                todos_proveedores.append(proveedor)
            
            if todos_proveedores:
                mejor_proveedor = min(
                    todos_proveedores,
                    key=lambda p: (
                        p.ultimo_precio * 
                        (1 + p.tiempo_entrega_avg.days * 0.02) *
                        (1 + (5 - p.rating) * 0.05)
                    )
                )
                
                cantidad = OptimizadorPedidos.calcular_cantidad(producto)
                
                sugerencias.append({
                    'producto': producto,
                    'proveedor': mejor_proveedor,
                    'cantidad': cantidad,
                    'precio_unitario': mejor_proveedor.ultimo_precio,
                    'motivo': 'Stock bajo' if producto.necesita_reabastecimiento() else 'Próximo a vencer',
                    'es_nuevo': mejor_proveedor not in proveedores_con_historial
                })
        
        return sugerencias
    
    @staticmethod
    def calcular_cantidad(producto):
        if producto.necesita_reabastecimiento():
            return max(
                producto.stock_minimo * 3 - producto.cantidad,
                producto.stock_minimo
            )
        return producto.stock_minimo