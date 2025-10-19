from django.urls import path
from .views import cliente, playero, crud_usuario
from .views.cliente import perfil, ver_puntos, tabla_puntos
from .views.playero import panel_playero
from .views.crud_usuario import register, login_view, logout_view, cambiar_contrasena
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cambiar-contrasena/', cambiar_contrasena, name='cambiar_contrasena'),
    path('perfil/', perfil, name='perfil'),
    path('mis-puntos/', ver_puntos, name='ver_puntos'),
    path('tabla/', tabla_puntos, name='tabla'),
    
    ## Weas de playero ##
    path('register/', crud_usuario.register, name='register'),
    path('login/', crud_usuario.login_view, name='login'),
    path('logout/', crud_usuario.logout_view, name='logout'),
    path('perfil/', cliente.perfil, name='perfil'),
    path('mis-puntos/', cliente.ver_puntos, name='ver_puntos'),
    path('playero/', playero.panel_playero, name='panel_playero'),
]