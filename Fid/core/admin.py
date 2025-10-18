from django.contrib import admin
from django.contrib.auth.models import User
from .models import Cliente

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'telefono', 'user', 'puntos', 'fecha_registro')

    # Sobreescribimos la creación para generar el User automáticamente
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            # Crear usuario automáticamente con DNI como username y contraseña
            user = User.objects.create_user(username=obj.dni, password=obj.dni)
            obj.user = user
        super().save_model(request, obj, form, change)

admin.site.register(Cliente, ClienteAdmin)
