import os
import re

trd_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\views.py'
with open(trd_path, 'r', encoding='utf8') as f:
    code = f.read()

if 'def is_trd_admin' not in code:
    code = code.replace("from django.http import JsonResponse, HttpResponse", 
"""from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

def is_trd_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.rol in ['SUPER', 'JEFE'])
""")
    
    # Proteger crear_oficina
    code = code.replace("def crear_oficina(request):",
"""def crear_oficina(request):
    if not is_trd_admin(request.user):
        messages.error(request, 'Solo el Administrador y el Jefe de Archivo pueden crear oficinas.')
        return redirect('trd:oficinas')
""")

    # Proteger eliminar_oficina
    code = code.replace("def eliminar_oficina(request, oficina_id):",
"""def eliminar_oficina(request, oficina_id):
    if not is_trd_admin(request.user):
        messages.error(request, 'No tienes permisos para eliminar oficinas.')
        return redirect('trd:oficinas')
""")

    # Proteger diligenciar (solo el POST)
    code = code.replace("if request.method == 'POST':",
"""if request.method == 'POST':
        if not is_trd_admin(request.user):
            messages.error(request, 'Solo el Jefe de Archivo puede guardar nuevas Tablas de Retención.')
            return redirect('trd:inicio')
""")

    # Proteger api_guardar_ccd_personalizado
    code = code.replace("def api_guardar_ccd_personalizado(request):",
"""def api_guardar_ccd_personalizado(request):
    if not is_trd_admin(request.user):
        return JsonResponse({'success': False, 'error': 'Permiso denegado.'}, status=403)
""")

    with open(trd_path, 'w', encoding='utf8') as f:
        f.write(code)
    print("Módulo TRD parcheado con seguridad de roles.")
