from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """Redirige a login si el usuario no está autenticado y no está en una URL pública."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        urls_publicas = [
            reverse('login'),
            reverse('register'),
            reverse('logout'),
        ]

        if not request.user.is_authenticated and path not in urls_publicas:
            return redirect('login')

        return self.get_response(request)
