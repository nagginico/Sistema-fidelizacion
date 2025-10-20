from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from ..models import Cliente, CargaCombustible
from django.contrib.auth.models import User



# --------------------------
# FUNCIÓN DE VALIDACIÓN
# --------------------------
def es_playero(user):
    """Verifica si el usuario autenticado tiene rol de playero."""
    try:
        return hasattr(user, "cliente") and user.cliente.es_playero
    except Cliente.DoesNotExist:
        return False


# --------------------------
# FUNCIÓN AUXILIAR
# --------------------------
def modificar_puntos(cliente, puntos, operacion, cargado_por):
    """Suma o resta puntos a un cliente y registra la acción."""
    if operacion == "sumar":
        cliente.puntos += puntos
        mensaje = f"Se sumaron {puntos} puntos a {cliente.dni}."
    elif operacion == "restar":
        cliente.puntos = max(0, cliente.puntos - puntos)
        mensaje = f"Se restaron {puntos} puntos a {cliente.dni}."
    else:
        return "Operación no válida."

    cliente.save()

    # Registrar carga
    CargaCombustible.objects.create(
        cliente=cliente,
        litros=puntos / 50,  # según tu regla: 1L = 50 puntos
        puntos_generados=puntos,
        cargado_por=cargado_por,
    )
    return mensaje


# --------------------------
# PANEL DEL PLAYERO
# --------------------------
@login_required
def panel_playero(request):
    """Vista principal del playero: búsqueda, suma/resta/eliminación."""
    if not es_playero(request.user):
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect("perfil")

    query = request.GET.get("q", "").strip()

    if query:
        clientes = (
            Cliente.objects
            .select_related("user")
            .filter(
                Q(dni__icontains=query) |
                Q(user__username__icontains=query)
            )
            .order_by("dni")
        )
    else:
        clientes = Cliente.objects.select_related("user").order_by("dni")

    if request.method == "POST":
        try:
            accion = request.POST.get("accion")
            cliente_id = request.POST.get("cliente_id")
            cliente = None

            if cliente_id:
                cliente = get_object_or_404(Cliente, id=cliente_id)

            if accion == "sumar" and cliente:
                puntos = int(request.POST.get("puntos", 0))
                mensaje = modificar_puntos(cliente, puntos, "sumar", request.user)
                messages.success(request, mensaje)

            elif accion == "restar" and cliente:
                puntos = int(request.POST.get("puntos", 0))
                mensaje = modificar_puntos(cliente, puntos, "restar", request.user)
                messages.warning(request, mensaje)

            elif accion == "eliminar" and cliente:
                cliente.delete()
                messages.info(request, f"Cliente {cliente.dni} eliminado correctamente.")

            elif accion == "agregar":
                dni = request.POST.get("dni")
                telefono = request.POST.get("telefono", "")

                if not dni:
                    messages.error(request, "Debe ingresar un DNI.")
                elif not Cliente.objects.filter(dni=dni).exists():
                    user = User.objects.create_user(username=dni, password=dni)
                    Cliente.objects.create(user=user, dni=dni, telefono=telefono, puntos=0)
                    messages.success(request, f"Cliente con DNI {dni} agregado.")
                else:
                    messages.error(request, "Ese cliente ya existe.")

            return redirect("panel_playero")

        except Exception as e:
            messages.error(request, f"Error del servidor: {str(e)}")
            return redirect("panel_playero")

    context = {
        "clientes": clientes,
        "query": query,
    }
    return render(request, "playero/panel_playero.html", context)
