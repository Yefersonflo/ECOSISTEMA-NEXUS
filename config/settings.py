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

# Cargar variables de entorno desde .env de forma nativa
import os
import json

env_file = BASE_DIR / '.env'
if env_file.exists():
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())
    except Exception:
        pass

# Modo de depuración: False en producción por defecto
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

# Clave secreta: SIEMPRE desde variable de entorno (nunca quemada en el código).
# En desarrollo se genera una efímera; en producción es OBLIGATORIA.
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        from django.core.management.utils import get_random_secret_key
        SECRET_KEY = get_random_secret_key()
    else:
        raise RuntimeError(
            'SECRET_KEY no está definida. Configúrala como variable de entorno en producción.'
        )

# Dominios o IPs permitidos para acceder a la aplicación
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', 'ecosistema-nexus-web.onrender.com,localhost,127.0.0.1,*')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]

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
    'config.middleware.SecurityHeadersMiddleware',  # CSP + Permissions-Policy
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
DATABASE_URL = os.environ.get('DATABASE_URL')

import dj_database_url
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Desarrollo local sin DATABASE_URL: SQLite (sin credenciales en el código).
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
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

# CONFIGURACIÓN DE REDIRECCIONES DE ACCESO
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# CONFIGURACIÓN DE ENVÍO DE CORREOS (SMTP / Consola para pruebas)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'radicacion@comfacasanare.com.co')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'tu_contrasena_segura')
DEFAULT_FROM_EMAIL = 'Nexus Comfacasanare <radicacion@comfacasanare.com.co>'

# Configuración de tipo de campo clave primaria predeterminado
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Blindaje de Cabeceras de Seguridad en Producción
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


