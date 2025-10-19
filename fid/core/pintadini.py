from django.shortcuts import redirect
from django.contrib import messages

def playero_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if hasattr(request.user, 'cliente') and request.user.cliente.is_playero:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "No tenés permisos para acceder a esta página.")
        return redirect('login')
    return wrapper
