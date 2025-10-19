from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Cliente
from ..utils.helpers import obtener_top_100


# --------------------------
# FUNCIÓN AUXILIAR
# --------------------------
def obtener_cliente_y_rol(request):
    """
    Retorna el objeto Cliente asociado al usuario y su rol (es_playero).
    Si no existe Cliente, lo crea automáticamente.
    """
    cliente, _ = Cliente.objects.get_or_create(
        user=request.user,
        defaults={
            "dni": request.user.username,
            "telefono": "",
        },
    )
    return cliente, cliente.es_playero


# --------------------------
# PERFIL DEL CLIENTE
# --------------------------
@login_required
def perfil(request):
    cliente, es_playero = obtener_cliente_y_rol(request)
    return render(request, "core/perfil.html", {
        "cliente": cliente,
        "es_playero": es_playero
    })


# --------------------------
# VER PUNTOS
# --------------------------
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Cliente

def inicio(request):
    """Página principal con ranking y acceso según autenticación."""
    # Obtener el top 10 de clientes ordenados por puntos
    top_clientes = Cliente.objects.order_by("-puntos")[:10]

    # Si el usuario está autenticado, mostrar sus puntos
    cliente = None
    if request.user.is_authenticated:
        try:
            cliente = request.user.cliente
        except Cliente.DoesNotExist:
            cliente = None

    context = {
        "cliente": cliente,
        "top_clientes": top_clientes,
    }

    return render(request, "core/inicio.html", context)

# --------------------------
# TABLA TOP 100
# --------------------------
@login_required
def tabla_puntos(request):
    top_100 = obtener_top_100()
    _, es_playero = obtener_cliente_y_rol(request)
    return render(request, "core/tabla.html", {
        "top_100": top_100,
        "es_playero": es_playero
    })
