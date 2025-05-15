from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from .models import Pedido, DetallePedido, Proveedor
from .forms import PedidoForm, DetallePedidoForm, ProveedorForm

@login_required
def pedido_list(request):
    estado = request.GET.get('estado', '')
    
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    
    if estado:
        pedidos = pedidos.filter(estado=estado)
    
    context = {
        'pedidos': pedidos,
        'estado_seleccionado': estado,
    }
    return render(request, 'pedidos/pedido_list.html', context)

@login_required
def pedido_create(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                pedido = form.save(commit=False)
                pedido.creado_por = request.user
                pedido.save()
                messages.success(request, f"Pedido #{pedido.id} creado exitosamente. Ahora puede agregar productos.")
                return redirect('pedido_detail', pk=pedido.pk)
    else:
        form = PedidoForm()
    return render(request, 'pedidos/pedido_form.html', {'form': form})

@login_required
def pedido_detail(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        form = DetallePedidoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                detalle = form.save(commit=False)
                detalle.pedido = pedido
                detalle.save()
                
                messages.success(request, "Producto agregado al pedido")
                return redirect('pedido_detail', pk=pedido.pk)
    else:
        form = DetallePedidoForm()
    
    detalles = pedido.detalles.all()
    total = detalles.aggregate(total=Sum('subtotal'))['total'] or 0
    
    context = {
        'pedido': pedido,
        'form': form,
        'detalles': detalles,
        'total': total,
    }
    return render(request, 'pedidos/pedido_detail.html', context)

@login_required
def cambiar_estado_pedido(request, pk, nuevo_estado):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if nuevo_estado == 'APROBADO' and pedido.puede_aprobar():
        pedido.estado = Pedido.EstadoPedido.APROBADO
        pedido.save()
        messages.success(request, f"Pedido #{pedido.id} aprobado exitosamente")
    
    elif nuevo_estado == 'RECIBIDO' and pedido.puede_recibir():
        with transaction.atomic():
            pedido.estado = Pedido.EstadoPedido.RECIBIDO
            pedido.fecha_recepcion = timezone.now().date()
            pedido.save()
            
            # Actualizar stock de productos
            for detalle in pedido.detalles.all():
                producto = detalle.producto
                producto.cantidad += detalle.cantidad
                producto.save()
            
            messages.success(request, f"Pedido #{pedido.id} recibido y stock actualizado")
    
    else:
        messages.error(request, f"No se puede cambiar el estado del pedido #{pedido.id}")
    
    return redirect('pedido_detail', pk=pedido.pk)

@login_required
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'pedidos/proveedor_list.html', {'proveedores': proveedores})

@login_required
def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor creado exitosamente")
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'pedidos/proveedor_form.html', {'form': form})

@login_required
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado exitosamente")
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'pedidos/proveedor_form.html', {'form': form})