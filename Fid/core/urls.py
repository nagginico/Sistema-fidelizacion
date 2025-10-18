from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('registrar-carga/', views.registrar_carga, name='registrar_carga'),  # Playero ingresa litros
]
