from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db import models 
from django.utils import timezone
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm


@login_required
def producto_list(request):
    query = request.GET.get('q', '')
    
    productos = Producto.objects.filter(
        Q(nombre__icontains=query) |
        Q(descripcion__icontains=query) |
        Q(categoria__nombre__icontains=query)
    ).order_by('nombre')
    
    productos_bajo_stock = Producto.objects.filter(
        cantidad__lte=models.F('stock_minimo'),
        estado='ACTIVO'
    )
    
    productos_proximos_vencer = Producto.objects.filter(
        fecha_vencimiento__lte=timezone.now() + timezone.timedelta(days=30),
        fecha_vencimiento__gte=timezone.now(),
        estado='ACTIVO'
    )
    
    context = {
        'productos': productos,
        'productos_bajo_stock': productos_bajo_stock,
        'productos_proximos_vencer': productos_proximos_vencer,
        'query': query,
    }
    return render(request, 'producto_list.html', context)

@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creado_por = request.user
            producto.save()
            messages.success(request, "Producto creado exitosamente")
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'producto_form.html', {'form': form})

@login_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente")
            return redirect('producto_detail', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto_form.html', {'form': form})

@login_required
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'producto_detail.html', {'producto': producto})

@login_required
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente")
            return redirect('categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'categoria_form.html', {'form': form})

@login_required
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada exitosamente")
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria_form.html', {'form': form})