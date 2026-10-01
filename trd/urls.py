from django.urls import path
from . import views

app_name = 'trd'

urlpatterns = [
    path('', views.diligenciar_trd, name='diligenciar'),
    path('exportar/', views.exportar_trd, name='exportar'),
]
