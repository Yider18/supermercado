from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/nuevo/', views.producto_create, name='producto_create'),
    path('productos/<int:pk>/', views.producto_detail, name='producto_detail'),
    path('productos/<int:pk>/editar/', views.producto_update, name='producto_update'),
    
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nuevo/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
]
