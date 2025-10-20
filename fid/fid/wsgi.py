import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fid.settings')
application = get_wsgi_application()

# Crear superusuario automáticamente solo en Render, FUNCIONO V:
if os.environ.get("RENDER"):
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from create_superuser import ensure_superuser
    ensure_superuser()


