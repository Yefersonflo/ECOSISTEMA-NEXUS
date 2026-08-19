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

# 2. Usuario Auxiliar Operativo (auxiliar / auxiliar123)
if not User.objects.filter(username='auxiliar').exists():
    user_aux = User.objects.create_user('auxiliar', 'auxiliar@comfacasanare.com.co', 'auxiliar123')
    Profile.objects.update_or_create(user=user_aux, defaults={'rol': 'JEFE', 'acceso_web': True})
    print("Usuario auxiliar creado exitosamente.")
else:
    user_aux = User.objects.get(username='auxiliar')
    user_aux.set_password('auxiliar123')
    user_aux.save()
    Profile.objects.update_or_create(user=user_aux, defaults={'rol': 'JEFE', 'acceso_web': True})
    print("Usuario auxiliar actualizado con contraseña auxiliar123.")
