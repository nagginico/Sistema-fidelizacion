from ..models import Cliente
from django.db.models import F

# -------------------------------------------------
# CALCULAR PUNTOS SEGÚN LITROS
# -------------------------------------------------
def calcular_puntos(litros):
    """Devuelve los puntos equivalentes a los litros cargados."""
    return int(litros * 50)


# -------------------------------------------------
# ACTUALIZAR PUNTOS DEL CLIENTE
# -------------------------------------------------
def agregar_puntos(cliente, litros):
    """Suma puntos al cliente según litros cargados."""
    puntos = calcular_puntos(litros)
    cliente.puntos = F('puntos') + puntos
    cliente.save(update_fields=['puntos'])
    cliente.refresh_from_db()
    return puntos


# -------------------------------------------------
# OBTENER TOP 100 CLIENTES
# -------------------------------------------------
def obtener_top_100():
    """Devuelve los 100 clientes con más puntos, mostrando solo los últimos 4 dígitos del teléfono."""
    clientes = Cliente.objects.order_by('-puntos')[:100]
    top = []
    for c in clientes:
        telefono_visible = f"****{c.telefono[-4:]}" if len(c.telefono) >= 4 else c.telefono
        top.append({
            'telefono': telefono_visible,
            'puntos': c.puntos,
        })
    return top
