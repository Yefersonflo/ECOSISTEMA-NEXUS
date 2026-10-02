from django.urls import path
from . import views, views_crud

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
    

    path('<int:enc_id>/nueva_version', views_crud.crear_nueva_version, name='crear_nueva_version'),
    path('<int:enc_id>/item', views_crud.crear_item, name='crear_item'),
    path('<int:enc_id>/serie/<int:serie_id>/agregar_subserie', views_crud.agregar_subserie_directa, name='agregar_subserie_directa'),
    path('<int:enc_id>/item/<int:padre_id>/agregar_tipo', views_crud.agregar_tipo_documental, name='agregar_tipo_documental'),
    path('<int:enc_id>/item/<int:item_id>/editar', views_crud.editar_campo_inline, name='editar_campo_inline'),
    path('<int:enc_id>/item/<int:item_id>/eliminar', views_crud.eliminar_item, name='eliminar_item'),

    # API endpoints
    path('api/ccd/oficina/<path:nombre_oficina>/', views.api_ccd_oficina, name='api_ccd_oficina'),
    path('api/ccd/guardar_personalizado/', views.api_guardar_ccd_personalizado, name='api_guardar_ccd_personalizado'),
    path('api/ccd/actualizar/', views.api_actualizar_ccd, name='api_actualizar_ccd'),
    path('api/ccd/eliminar/', views.api_eliminar_ccd, name='api_eliminar_ccd'),
]
