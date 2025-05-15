from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import Usuario
from .forms import LoginForm, RegistroForm, UsuarioForm
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"¡Bienvenido {user.get_full_name()}!")
                return redirect('inicio')
        messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.es_administrador())
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Usuario {user.username} registrado exitosamente!")
            return redirect('usuario_list')
    else:
        form = RegistroForm()
    return render(request, 'usuario_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.es_administrador())
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario_list.html', {'usuarios': usuarios})

@login_required
@user_passes_test(lambda u: u.es_administrador())
def usuario_update(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado exitosamente")
            return redirect('usuario_list')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuario_form.html', {'form': form})
@login_required
def logout_view(request):
    """Vista para cerrar sesión (solo POST por seguridad)"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Has cerrado sesión correctamente")
        return redirect('inicio')  # Cambiado a nombre de URL en vez de template
    else:
        # Si se accede por GET, redirigir al inicio o mostrar formulario
        return render(request, 'logout_confirmation.html')  # Crea este template
def es_administrador(user):
    """Función helper para verificar si el usuario es administrador"""
    return user.is_authenticated and user.es_administrador()
# Create your views here.
