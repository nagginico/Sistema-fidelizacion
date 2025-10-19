from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Cliente
from ..utils.helpers import obtener_top_100

# --------------------------
# PERFIL DEL CLIENTE
# --------------------------
@login_required
def perfil(request):
    cliente = request.user.cliente
    return render(request, "core/perfil.html", {"cliente": cliente})


# --------------------------
# VER PUNTOS
# --------------------------
@login_required
def ver_puntos(request):
    cliente = request.user.cliente
    return render(request, "core/puntos.html", {"puntos": cliente.puntos})


# --------------------------
# TABLA TOP 100
# --------------------------
@login_required
def tabla_puntos(request):
    top_100 = obtener_top_100()
    return render(request, "core/tabla.html", {"top_100": top_100})
