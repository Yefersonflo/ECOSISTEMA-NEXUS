from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views, logout

class CustomLoginView(auth_views.LoginView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_superuser:
            if not hasattr(user, 'profile') or not user.profile.acceso_web:
                form.add_error(None, "Su usuario no tiene autorización para acceder a la plataforma web.")
                return self.form_invalid(form)
        return super().form_valid(form)

from afiliados.views import (
    dashboard, detalle_carpeta, borrar_documento, borrar_carpeta, 
    mapa_visual, gestion_documental, panel_reportes, exportar_excel_archivo,
    historial_auditoria, exportar_auditoria_excel, api_buscar_afiliado, api_sincronizar_afiliados
)
from django.conf import settings
from django.conf.urls.static import static

# Definición de las rutas (URLs) del proyecto y su mapeo a las vistas
urlpatterns = [
    # Interfaz de administración predeterminada de Django
    path('admin/', admin.site.urls),
    # API JSON para Gestor de Escritorio remoto
    path('api/buscar/', api_buscar_afiliado, name='api_buscar_afiliado'),
    path('api/sincronizar/', api_sincronizar_afiliados, name='api_sincronizar_afiliados'),
    # Página de inicio / Panel de control principal
    path('', dashboard, name='dashboard'),
    # Gestión de sesiones (Inicio y cierre de sesión)
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # SECCIÓN: GESTIÓN DOCUMENTAL (ARCHIVO FÍSICO)
    # Panel principal de gestión de archivos y carpetas
    path('gestion-documental/', gestion_documental, name='gestion_documental'),
    # Consulta de contenidos de una carpeta específica
    path('dashboard/folder/<int:carpeta_id>/', detalle_carpeta, name='detalle_carpeta'),
    # Eliminación de carpetas (Acceso restringido)
    path('dashboard/folder/delete/<int:carpeta_id>/', borrar_carpeta, name='borrar_carpeta'),
    # Eliminación de documentos individuales
    path('dashboard/document/delete/<int:doc_id>/', borrar_documento, name='borrar_documento'),
    # Visualización gráfica de la ubicación física de las carpetas
    path('mapa-visual/', mapa_visual, name='mapa_visual'),
    # Panel para generación de reportes y estadísticas
    path('reportes-registros/', panel_reportes, name='panel_reportes'),
    # Descarga de inventario de archivo en formato Excel
    path('exportar-excel-archivo/', exportar_excel_archivo, name='exportar_excel_archivo'),

    # Módulo de Auditoría Global (Superusuario)
    path('historial-auditoria/', historial_auditoria, name='historial_auditoria'),
    path('historial-auditoria/exportar/', exportar_auditoria_excel, name='exportar_auditoria_excel'),

    # SECCIÓN DE SEGURIDAD ELIMINADA DE URLS (Manejado por /admin/)
]

# Configuración para servir archivos multimedia en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)