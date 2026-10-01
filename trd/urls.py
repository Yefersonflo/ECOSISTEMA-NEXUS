from django.urls import path
from . import views

app_name = 'trd'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('diligenciar/', views.diligenciar, name='diligenciar'),
    path('<int:enc_id>/', views.editar_trd, name='editar_trd'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('oficinas/', views.oficinas, name='oficinas'),
    path('oficinas/nueva/', views.crear_oficina, name='crear_oficina'),
    path('oficinas/<int:oficina_id>/eliminar/', views.eliminar_oficina, name='eliminar_oficina'),
    path('exportar/<int:enc_id>/', views.exportar, name='exportar'),
    path('exportar_pdf/<int:enc_id>/', views.exportar_pdf, name='exportar_pdf'),
    
    # API endpoints
    path('api/ccd/oficina/<path:nombre_oficina>/', views.api_ccd_oficina, name='api_ccd_oficina'),
    path('api/ccd/guardar_personalizado/', views.api_guardar_ccd_personalizado, name='api_guardar_ccd_personalizado'),
    path('api/ccd/actualizar/', views.api_actualizar_ccd, name='api_actualizar_ccd'),
    path('api/ccd/eliminar/', views.api_eliminar_ccd, name='api_eliminar_ccd'),
]
