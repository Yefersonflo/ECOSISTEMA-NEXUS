from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Carpeta, Profile, HistorialCarpeta

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)

@admin.register(Carpeta)
class CarpetaAdmin(admin.ModelAdmin):
    search_fields = ('identificacion', 'nombre')
    list_display = ('identificacion', 'nombre', 'modulo', 'estante', 'bandeja', 'cubiculo', 'numero_carpeta', 'estado')

@admin.register(HistorialCarpeta)
class HistorialCarpetaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'carpeta')