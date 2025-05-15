from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.pedido_list, name='pedido_list'),
    path('nuevo/', views.pedido_create, name='pedido_create'),
    path('<int:pk>/', views.pedido_detail, name='pedido_detail'),
    path('<int:pk>/estado/<str:nuevo_estado>/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/nuevo/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/<int:pk>/editar/', views.proveedor_update, name='proveedor_update'),
]