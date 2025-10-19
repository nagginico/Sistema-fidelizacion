from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib import messages
from ..forms import RegistroClienteForm, LoginForm, CambioPasswordForm
from django.contrib.auth.decorators import login_required

# --------------------------
# registrro
# --------------------------
def register(request):
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada correctamente. Ya podes iniciar sesión.")
            return redirect("login")
    else:
        form = RegistroClienteForm()
    return render(request, "core/registro.html", {"form": form})


# --------------------------
# inicio
# --------------------------

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}")
            return redirect("perfil")
    else:
        form = LoginForm()

    # Verificar si el usuario autenticado pertenece al grupo "playero"
    es_playero = False
    if request.user.is_authenticated:
        es_playero = request.user.groups.filter(name="playero").exists()

    return render(request, "core/login.html", {
        "form": form,
        "es_playero": es_playero,
    })



# --------------------------
# se sale
# --------------------------
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect("login")


# --------------------------
# cambio de datos (falta actualizar datos del perfil)
# --------------------------
@login_required
def cambiar_contrasena(request):
    if request.method == "POST":
        form = CambioPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Contraseña cambiada correctamente")
            return redirect("perfil")
    else:
        form = CambioPasswordForm(user=request.user)
    return render(request, "core/cambiar_contrasena.html", {"form": form})
