from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Cliente
from django.db.models import Q

# Verificar si el usuario pertenece al grupo 'playero'
def es_playero(user):
    return user.groups.filter(name='playero').exists()


@login_required
@user_passes_test(es_playero)
def panel_playero(request):
    # --- Buscar por DNI o nombre ---
    query = request.GET.get('q', '')
    clientes = Cliente.objects.filter(
        Q(dni__icontains=query) | Q(user__username__icontains=query)
    ).order_by('user__username') if query else Cliente.objects.all().order_by('user__username')

    # --- Agregar cliente ---
    if request.method == 'POST' and 'agregar_cliente' in request.POST:
        username = request.POST.get('username')
        dni = request.POST.get('dni')
        puntos = int(request.POST.get('puntos', 0))

        # Evitar duplicados
        if not Cliente.objects.filter(dni=dni).exists():
            Cliente.objects.create(
                user=None,  # si lo vinculas luego al User, podés agregarlo aquí
                dni=dni,
                puntos=puntos
            )

    # --- Sumar puntos ---
    if request.method == 'POST' and 'sumar_puntos' in request.POST:
        cliente_id = request.POST.get('cliente_id')
        puntos = int(request.POST.get('puntos', 0))
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.puntos += puntos
        cliente.save()

    # --- Restar puntos ---
    if request.method == 'POST' and 'restar_puntos' in request.POST:
        cliente_id = request.POST.get('cliente_id')
        puntos = int(request.POST.get('puntos', 0))
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.puntos = max(0, cliente.puntos - puntos)
        cliente.save()

    # --- Eliminar cliente ---
    if request.method == 'POST' and 'eliminar_cliente' in request.POST:
        cliente_id = request.POST.get('cliente_id')
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente.delete()

    context = {
        'clientes': clientes,
        'query': query,
    }
    return render(request, 'playero/panel_playero.html', context)
