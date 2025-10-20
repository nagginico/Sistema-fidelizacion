from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import RegistroClienteForm, LoginForm, CambioPasswordForm
from ..models import Cliente
from django.contrib.auth.forms import PasswordChangeForm

# --------------------------
def register(request):
    """Permite registrar un nuevo cliente."""
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada correctamente. Ya podés iniciar sesión.")
            return redirect("login")
        else:
            messages.error(request, "Hubo un error en el formulario. Revisá los datos.")
    else:
        form = RegistroClienteForm()

    return render(request, "core/registro.html", {"form": form})



# --------------------------

def login_view(request):
    next_url = request.GET.get("next")  # detecta si fue redirigido
    mensaje = None

    if next_url:
        mensaje = "Debes iniciar sesión para continuar."

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}")
            return redirect(next_url or "perfil")  # si lo es, va a ese url
    else:
        form = LoginForm()

    return render(request, "core/login.html", {"form": form, "mensaje": mensaje})


# --------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect("login")



# --------------------------

@login_required
def cambiar_contrasena(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # mantiene la sesión activa
            messages.success(request, "Tu contraseña fue actualizada correctamente.")
            return redirect("perfil")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, "core/perfil.html", {"form_cambio_pass": form})