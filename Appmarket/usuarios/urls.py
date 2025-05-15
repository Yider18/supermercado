from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/nuevo/', views.registro_usuario, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    
]