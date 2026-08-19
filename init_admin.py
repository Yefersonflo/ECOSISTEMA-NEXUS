from django.contrib.auth.models import User
from afiliados.models import Profile

# 1. Superusuario Administrador (admin / admin123)
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@comfacasanare.com.co', 'admin123')
    Profile.objects.update_or_create(user=user, defaults={'rol': 'SUPER', 'acceso_web': True})
    print("Superusuario admin creado exitosamente.")
else:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    Profile.objects.update_or_create(user=user, defaults={'rol': 'SUPER', 'acceso_web': True})
    print("Superusuario admin actualizado.")

# 2. Usuarios Auxiliares Operativos
aux_users = [
    ('SandraP', 'SandraP123', 'sandrap@comfacasanare.com.co'),
    ('NicolasB', 'NicolasB123', 'nicolasb@comfacasanare.com.co'),
    ('JairN', 'JairN123', 'jairn@comfacasanare.com.co'),
    ('AndresL', 'AndresL123', 'andresl@comfacasanare.com.co'),
]

for username, password, email in aux_users:
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.update_or_create(user=u, defaults={'rol': 'JEFE', 'acceso_web': True})
        print(f"Usuario {username} creado exitosamente.")
    else:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        Profile.objects.update_or_create(user=u, defaults={'rol': 'JEFE', 'acceso_web': True})
        print(f"Usuario {username} actualizado exitosamente.")
