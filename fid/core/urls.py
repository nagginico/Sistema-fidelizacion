from django.urls import path
from .views.crud_usuario import login_view, register, logout_view, cambiar_contrasena
from .views.cliente import inicio, perfil
from .views.playero import panel_playero

urlpatterns = [
    # -----------------------
    # Página principal (tabla general)
    # -----------------------
    path("", inicio, name="inicio"),
    path("cambiar-contrasena/", cambiar_contrasena, name="cambiar_contrasena"),

    # -----------------------
    # Autenticación
    # -----------------------
    path("login/", login_view, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),

    # -----------------------
    # Perfil de usuario
    # -----------------------
    path("perfil/", perfil, name="perfil"),

    # -----------------------
    # Panel del playero
    # -----------------------
    path("playero/", panel_playero, name="panel_playero"),
]
