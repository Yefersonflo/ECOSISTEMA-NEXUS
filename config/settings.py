"""
Configuración principal de Django para el proyecto archivo_caja.
Este archivo contiene todos los parámetros de comportamiento del framework.
"""

from pathlib import Path
import copy

# Patch Python 3.14 incompatibility with Django Template Context __copy__
try:
    from django.template import context
    def _safe_context_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        if hasattr(self, '__dict__'):
            duplicate.__dict__.update(self.__dict__)
        duplicate.dicts = [d.copy() for d in getattr(self, 'dicts', [])]
        if hasattr(self, 'render_context'):
            duplicate.render_context = copy.copy(self.render_context)
        return duplicate

    context.BaseContext.__copy__ = _safe_context_copy
    context.Context.__copy__ = _safe_context_copy
    context.RequestContext.__copy__ = _safe_context_copy
except Exception:
    pass

# Define la ruta base del proyecto para referenciar carpetas internas
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de seguridad: Clave secreta para criptografía en el sitio
SECRET_KEY = 'django-insecure--roagn(!n==-+^85i*f)f^%q@3h4zv^b@!*2qb%xil3x-xhmo&'

# Modo de depuración: True para desarrollo, False para producción
DEBUG = True

# Dominios o IPs permitidos para acceder a la aplicación
ALLOWED_HOSTS = ['*']

# Definición de aplicaciones instaladas (módulos internos y externos)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicaciones del proyecto
    'ubicacion',
    'afiliados',
    'documentos',
    'smart_selects' # Librería para selects encadenados
]

# Capas de procesamiento para peticiones y respuestas
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'afiliados.middleware.ActiveUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Archivo principal de configuración de URLs
ROOT_URLCONF = 'config.urls'

# Configuración del motor de plantillas HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Directorio global de plantillas
        'APP_DIRS': True, # Busca plantillas dentro de cada aplicación
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Punto de entrada para servidores web WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# Configuración de la base de datos (PostgreSQL en la Nube / SQLite en local)
import os
import json

DEFAULT_RENDER_DB_URL = "postgresql://nexus_postgres_db_user:cU0VInNSTcc69JZbDtuVnp2gOJx0AJEV@dpg-da2ssrflk1mc73cq2960-a.oregon-postgres.render.com/nexus_postgres_db"
DATABASE_URL = os.environ.get('DATABASE_URL', DEFAULT_RENDER_DB_URL)

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Validadores para asegurar la fortaleza de las contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de localización e idioma (Español Colombia)
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Gestión de archivos estáticos (CSS, JS) y multimedia (Uploads)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CONFIGURACIÓN DE CORREO INSTITUCIONAL (Sincronización IMAP)
IMAP_SERVER = 'comfacasanare.com.co'
IMAP_USER = 'jefersonflores@comfacasanare.com.co'
IMAP_PASS = 'JefersonFlores2026$%'

# CONFIGURACIÓN DE REDIRECCIONES DE ACCESO
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# CONFIGURACIÓN DE ENVÍO DE CORREOS (SMTP / Consola para pruebas)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'radicacion@comfacasanare.com.co'
EMAIL_HOST_PASSWORD = 'tu_contrasena_segura'
DEFAULT_FROM_EMAIL = 'Nexus Comfacasanare <radicacion@comfacasanare.com.co>'

# Configuración de tipo de campo clave primaria predeterminado
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

