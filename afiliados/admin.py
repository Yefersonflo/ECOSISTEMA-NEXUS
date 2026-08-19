from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Carpeta, Profile, HistorialCarpeta

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

# Re-registrar el modelo de Usuario con el perfil embebido
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Carpeta)
admin.site.register(HistorialCarpeta)