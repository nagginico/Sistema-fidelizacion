from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'dni', 'telefono', 'es_playero', 'puntos')
    list_editable = ('es_playero',)  # <-- aquí permitimos cambiarlo desde la lista
    list_filter = ('es_playero',)
    search_fields = ('user__username', 'dni', 'telefono')