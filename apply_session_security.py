import os
import re

settings_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\config\settings.py'

with open(settings_path, 'r', encoding='utf8') as f:
    code = f.read()

# Reemplazar la sección de sesión actual por la nueva configuración completa
old_session = "SESSION_EXPIRE_AT_BROWSER_CLOSE = True"
new_session = """# ==========================================
# CONFIGURACIÓN DE SEGURIDAD DE SESIONES
# ==========================================
# 1. Cerrar sesión al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 2. Expirar la sesión después de 30 minutos de inactividad (1800 segundos)
SESSION_COOKIE_AGE = 1800 

# 3. Renovar los 30 minutos cada vez que el usuario hace clic o navega en la plataforma
SESSION_SAVE_EVERY_REQUEST = True"""

if old_session in code:
    code = code.replace(old_session, new_session)
    with open(settings_path, 'w', encoding='utf8') as f:
        f.write(code)
    print("Configuración de sesiones aplicada.")
else:
    print("No se encontró SESSION_EXPIRE_AT_BROWSER_CLOSE")
