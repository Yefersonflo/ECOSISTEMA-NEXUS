from django.contrib.auth.models import User
from afiliados.models import Profile

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@comfacasanare.com.co', 'admin123')
    Profile.objects.update_or_create(user=user, defaults={'rol': 'SUPER', 'acceso_web': True})
    print("Superusuario admin creado exitosamente.")
else:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    Profile.objects.update_or_create(user=user, defaults={'rol': 'SUPER', 'acceso_web': True})
    print("Superusuario admin actualizado con contraseña admin123.")
