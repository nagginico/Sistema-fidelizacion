from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Cliente

@login_required
def perfil(request):
    """Vista del perfil del cliente o playero, permite editar datos personales."""
    cliente = request.user.cliente

    # Obtener posición del ranking
    ranking = list(
        Cliente.objects.order_by("-puntos").values_list("id", flat=True)
    )
    posicion = ranking.index(cliente.id) + 1 if cliente.id in ranking else "—"

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        apellido = request.POST.get("apellido", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        email = request.POST.get("email", "").strip()

        # Actualizar datos
        cliente.telefono = telefono
        cliente.save()

        request.user.first_name = nombre
        request.user.last_name = apellido
        request.user.email = email
        request.user.save()

        messages.success(request, "Datos actualizados correctamente.")
        return redirect("perfil")

    context = {
        "cliente": cliente,
        "posicion": posicion,
    }
    return render(request, "core/perfil.html", context)


def inicio(request):
    """Página principal visible para todos (logueados o no)."""
    # Mostrar los primeros 10 del ranking
    top_clientes = Cliente.objects.filter(es_playero=False).order_by("-puntos")

    user_cliente = None
    posicion = None

    if request.user.is_authenticated:
        user_cliente = getattr(request.user, "cliente", None)
        if user_cliente:
            ranking = list(Cliente.objects.order_by('-puntos').values_list('id', flat=True))
            posicion = ranking.index(user_cliente.id) + 1 if user_cliente.id in ranking else None

    context = {
        "top_clientes": top_clientes,
        "user_cliente": user_cliente,
        "posicion": posicion,
    }
    return render(request, "core/inicio.html", context)
