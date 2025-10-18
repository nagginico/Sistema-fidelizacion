from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    dni = models.CharField(max_length=20, unique=True)
    puntos = models.IntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dni} ({self.puntos} pts)"

class Carga(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    litros = models.PositiveIntegerField()
    puntos_obtenidos = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.puntos_obtenidos = self.litros * 50  # 1 litro = 50 puntos
        super().save(*args, **kwargs)
        # Sumar puntos al cliente
        self.cliente.puntos += self.puntos_obtenidos
        self.cliente.save()
