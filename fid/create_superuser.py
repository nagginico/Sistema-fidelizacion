from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

username = "naggi"
email = "nagginico@gmail.com"
password = "44033699"

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superusuario creado con éxito.")
    else:
        print("ℹEl superusuario ya existe.")
except IntegrityError:
    print("No se pudo crear el superusuario (posible duplicado).")
