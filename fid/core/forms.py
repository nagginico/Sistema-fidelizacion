from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import Cliente

# -------------------------------------------------
# FORMULARIO DE REGISTRO DE CLIENTE
# -------------------------------------------------
class RegistroClienteForm(forms.ModelForm):
    dni = forms.CharField(max_length=20, required=True, label="DNI")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Contraseña")

    class Meta:
        model = Cliente
        fields = ['dni', 'telefono']

    def save(self, commit=True):
        """Crea el usuario y el cliente asociado"""
        dni = self.cleaned_data['dni']
        password = self.cleaned_data['password'] or dni  # si no escribe, usa el DNI
        telefono = self.cleaned_data['telefono']

        user = User.objects.create_user(username=dni, password=password)
        cliente = Cliente(user=user, dni=dni, telefono=telefono)

        if commit:
            user.save()
            cliente.save()

        return cliente

class PlayeroEditarClienteForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Cliente
        fields = ['telefono', 'tiene_auto', 'tiene_moto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        cliente = super().save(commit=False)
        if self.instance.user:
            self.instance.user.first_name = self.cleaned_data['first_name']
            self.instance.user.last_name = self.cleaned_data['last_name']
            self.instance.user.email = self.cleaned_data['email']
            if commit:
                self.instance.user.save()
                cliente.save()
        return cliente
    
# -------------------------------------------------
# FORMULARIO DE LOGIN
# -------------------------------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="DNI")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


# -------------------------------------------------
# FORMULARIO DE CAMBIO DE CONTRASEÑA
# -------------------------------------------------
class CambioPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Contraseña actual")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Nueva contraseña")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar nueva contraseña")
