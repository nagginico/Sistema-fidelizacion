from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    puntos = models.PositiveIntegerField(default=0)
    es_playero = models.BooleanField(default=False)

   
    tiene_auto = models.BooleanField(default=False)
    tiene_moto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username if self.user else 'Sin usuario'} - {self.dni}"



class CargaCombustible(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    litros = models.DecimalField(max_digits=6, decimal_places=2)
    puntos_generados = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    # quién hizo la carga si cliente o usuario
    cargado_por = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="cargas_realizadas"
    )

    def __str__(self):
        return f"{self.cliente.dni} - {self.litros}L - {self.puntos_generados}pts"