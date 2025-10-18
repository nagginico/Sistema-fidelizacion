from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, LoginForm, CargaForm
from .models import Cliente

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = RegistroForm(request.POST)
            if form.is_valid():
                form.save()
                dni = form.cleaned_data['dni']
                user = authenticate(username=dni, password=form.cleaned_data.get('password') or dni)
                login(request, user)
                return redirect('dashboard')
        else:
            form = RegistroForm()
    return render(request, 'core/home.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    cliente = request.user.cliente
    # Top 100 clientes ordenados por puntos descendente
    top_100 = Cliente.objects.order_by('-puntos')[:100]
    return render(request, 'core/dashboard.html', {'cliente': cliente, 'top_100': top_100})

@login_required
def cambiar_password(request):
    from django.contrib.auth.forms import PasswordChangeForm
    from django.contrib.auth import update_session_auth_hash

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/cambiar_password.html', {'form': form})

@login_required
def registrar_carga(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        litros = int(request.POST.get('litros'))
        if litros < 1:
            litros = 1
        cliente = get_object_or_404(Cliente, dni=dni)
        cliente.carga_set.create(litros=litros)
        return redirect('dashboard')
    return render(request, 'core/registrar_carga.html')
