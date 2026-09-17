"""
Middleware de cabeceras de seguridad.

Añade las cabeceras que Django no incluye por defecto: Content-Security-Policy
y Permissions-Policy. Se aplican en toda respuesta (independiente de DEBUG).
Nota: HSTS, cookies seguras y redirección SSL ya se configuran en settings.py
dentro del bloque `if not DEBUG` (requiere DEBUG=False en producción).
"""

# CSP de arranque: permisiva con estilos/scripts inline para no romper la UI.
# Endurécela progresivamente (quita 'unsafe-inline') revisando la consola del navegador.
_CSP = (
    "default-src 'self'; "
    "img-src 'self' data: https:; "
    "style-src 'self' 'unsafe-inline' https:; "
    "script-src 'self' 'unsafe-inline' https:; "
    "font-src 'self' data: https:; "
    "frame-ancestors 'none'"
)
_PERMISSIONS = "geolocation=(), microphone=(), camera=(), payment=()"


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not response.has_header("Content-Security-Policy"):
            response["Content-Security-Policy"] = _CSP
        if not response.has_header("Permissions-Policy"):
            response["Permissions-Policy"] = _PERMISSIONS
        return response
