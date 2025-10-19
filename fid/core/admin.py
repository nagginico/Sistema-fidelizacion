from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'dni', 'telefono', 'is_playero', 'puntos')
    list_editable = ('is_playero',)  # <-- aquí permitimos cambiarlo desde la lista
    list_filter = ('is_playero',)
    search_fields = ('user__username', 'dni', 'telefono')