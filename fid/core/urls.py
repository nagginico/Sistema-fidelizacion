from django.urls import path
from .views.crud_usuario import register, login_view, logout_view, cambiar_contrasena
from .views.cliente import perfil, tabla_puntos, inicio
from .views.playero import panel_playero

urlpatterns = [
    # Página de inicio (todos pueden verla)
    path("", inicio, name="inicio"),

    # Autenticación
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("cambiar-contrasena/", cambiar_contrasena, name="cambiar_contrasena"),

    # Cliente
    path("perfil/", perfil, name="perfil"),
    path("tabla/", tabla_puntos, name="tabla"),

    # Playero
    path("playero/", panel_playero, name="panel_playero"),
]

