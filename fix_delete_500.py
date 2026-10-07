import os

views_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\views.py'

with open(views_path, 'r', encoding='utf8') as f:
    views_code = f.read()

# Arreglar la función eliminar_trd
viejo_codigo = """
def eliminar_trd(request, enc_id):
    if not is_trd_admin(request.user):
        messages.error(request, 'No tienes permisos para eliminar Tablas de Retención.')
        return redirect('trd:inicio')
    from django.shortcuts import get_object_or_404
    from .models import TRDEncabezado
    try:
        trd = get_object_or_404(TRDEncabezado, id=enc_id)
        nombre = f"{trd.oficina.nombre} (V{trd.version})"
        trd.delete()
        messages.success(request, f'La TRD de {nombre} fue eliminada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar TRD: {str(e)}')
    return redirect('trd:inicio')
"""

nuevo_codigo = """
def eliminar_trd(request, enc_id):
    if not is_trd_admin(request.user):
        messages.error(request, 'No tienes permisos para eliminar Tablas de Retención.')
        return redirect('trd:inicio')
    from django.shortcuts import get_object_or_404
    from .models import EncabezadoTRD
    try:
        trd = get_object_or_404(EncabezadoTRD, id=enc_id)
        nombre = f"{trd.oficina_productora} (V{trd.version})"
        trd.delete()
        messages.success(request, f'La TRD de {nombre} fue eliminada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar TRD: {str(e)}')
    return redirect('trd:inicio')
"""

if viejo_codigo.strip() in views_code:
    views_code = views_code.replace(viejo_codigo.strip(), nuevo_codigo.strip())
    with open(views_path, 'w', encoding='utf8') as f:
        f.write(views_code)
    print("Corrección aplicada correctamente.")
else:
    print("No se encontró el código viejo para reemplazar.")
