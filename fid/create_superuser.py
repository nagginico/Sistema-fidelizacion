from django.contrib.auth import get_user_model

User = get_user_model()

def ensure_superuser():
    username = "admin"
    email = "admin@example.com"
    password = "admin1234"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superusuario creado correctamente.")
    else:
        print("ℹEl superusuario ya existe.")

ensure_superuser()
