from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from django.utils.translation import gettext_lazy as _

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    telefono = forms.CharField(required=False)
    direccion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), 
        required=False
    )
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y']
    )
    
    class Meta:
        model = Usuario
        fields = (
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2',
            'tipo_usuario',
            'telefono',
            'direccion',
            'fecha_nacimiento'
        )
        labels = {
            'tipo_usuario': _('Tipo de Usuario')
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Usuario'),
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label=_('Contraseña'),
        strip=False,
        widget=forms.PasswordInput
    )

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'tipo_usuario',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'is_active'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3})
        }
        