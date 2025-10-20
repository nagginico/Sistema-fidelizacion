from django.urls import path
from .views.crud_usuario import register, login_view, logout_view, cambiar_contrasena
from .views.cliente import perfil, inicio
from .views.playero import panel_playero

urlpatterns = [
    # Página de inicio (visible para todos)
    path("", inicio, name="inicio"),

    # Autenticación
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("cambiar-contrasena/", cambiar_contrasena, name="cambiar_contrasena"),

    # Cliente / perfil
    path("perfil/", perfil, name="perfil"),

    # Panel del playero
    path("playero/", panel_playero, name="panel_playero"),
]
