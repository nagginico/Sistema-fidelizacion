from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    puntos = models.IntegerField(default=0)
    tiene_auto = models.BooleanField(default=False)
    tiene_moto = models.BooleanField(default=False)
    is_playero = models.BooleanField(default=False)

    
class CargaCombustible(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    litros = models.DecimalField(max_digits=6, decimal_places=2)
    puntos_generados = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.dni} - {self.litros}L - {self.puntos_generados}pts"

class Playero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    is_playero = models.BooleanField(default=False)  # nadie tiene permiso al registrarse


    def __str__(self):
        return self.nombre

