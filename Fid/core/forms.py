from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente, Carga

class RegistroForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    telefono = forms.CharField(required=True)
    dni = forms.CharField(required=True)

    class Meta:
        model = User
        fields = []

    def save(self, commit=True):
        dni = self.cleaned_data['dni']
        telefono = self.cleaned_data['telefono']
        password = self.cleaned_data.get('password') or dni  # contraseña = DNI si está en blanco

        # Crear usuario
        user = User.objects.create_user(username=dni, password=password)
        
        # Crear cliente
        cliente = Cliente.objects.create(
            user=user,
            dni=dni,
            telefono=telefono
        )
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='DNI')
    password = forms.CharField(widget=forms.PasswordInput)

class CargaForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = ['litros']
