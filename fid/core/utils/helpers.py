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

def obtener_top_100():
    return Cliente.objects.order_by("-puntos")[:100]