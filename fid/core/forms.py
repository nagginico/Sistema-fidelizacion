from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import Cliente

# -------------------------------------------------
# FORMULARIO DE REGISTRO DE CLIENTE
# -------------------------------------------------
from django import forms
from django.contrib.auth.models import User
from .models import Cliente

class RegistroClienteForm(forms.ModelForm):
    dni = forms.CharField(max_length=20, required=True, label="DNI")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono")
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Contraseña (solo si ya tenés usuario)"
    )

    class Meta:
        model = Cliente
        fields = ["dni", "telefono"]

    def clean_dni(self):
        dni = self.cleaned_data["dni"]
        if not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo números.")
        return dni

    def clean(self):
        """Verifica si el usuario ya existe y ajusta las validaciones."""
        cleaned_data = super().clean()
        dni = cleaned_data.get("dni")
        password = cleaned_data.get("password")

        if User.objects.filter(username=dni).exists():
            # Si ya existe → contraseña es obligatoria
            if not password:
                self.add_error("password", "Debes ingresar tu nueva contraseña.")
        return cleaned_data

    def save(self, commit=True):
        dni = self.cleaned_data["dni"]
        telefono = self.cleaned_data["telefono"]
        password = self.cleaned_data["password"] or dni  # por defecto, usa el DNI

        if User.objects.filter(username=dni).exists():
            # Si el usuario ya existe → actualiza contraseña y teléfono
            user = User.objects.get(username=dni)
            if self.cleaned_data["password"]:
                user.set_password(password)
            user.save()

            cliente, _ = Cliente.objects.get_or_create(user=user)
            cliente.telefono = telefono
            if commit:
                cliente.save()
        else:
            # Si no existe → crea usuario + cliente nuevo
            user = User.objects.create_user(username=dni, password=password)
            cliente = Cliente(user=user, dni=dni, telefono=telefono)
            if commit:
                user.save()
                cliente.save()

        return cliente



# -------------------------------------------------
# FORMULARIO DE EDICIÓN SOLO PA PLAYEROS
# -------------------------------------------------
class PlayeroEditarClienteForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label="Nombre")
    last_name = forms.CharField(required=False, label="Apellido")
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = Cliente
        fields = ["telefono"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.user:
            self.fields["first_name"].initial = self.instance.user.first_name
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        cliente = super().save(commit=False)
        if self.instance.user:
            self.instance.user.first_name = self.cleaned_data["first_name"]
            self.instance.user.last_name = self.cleaned_data["last_name"]
            self.instance.user.email = self.cleaned_data["email"]
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
# FORMULARIO DE CAMBIO DE CONTRASEÑA ACTUALIZA DESPUES PARA MAS DATOS
# -------------------------------------------------
class CambioPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Contraseña actual")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Nueva contraseña")
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar nueva contraseña"
    )
