import os
import re

base_dir = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd'
views_path = os.path.join(base_dir, 'views.py')
urls_path = os.path.join(base_dir, 'urls.py')
template_path = os.path.join(base_dir, 'templates', 'trd', 'inicio.html')

# 1. Modificar views.py
with open(views_path, 'r', encoding='utf8') as f:
    views_code = f.read()

if 'def eliminar_trd(' not in views_code:
    new_view = """
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
    views_code += new_view
    with open(views_path, 'w', encoding='utf8') as f:
        f.write(views_code)

# 2. Modificar urls.py
with open(urls_path, 'r', encoding='utf8') as f:
    urls_code = f.read()

if 'eliminar_trd' not in urls_code:
    urls_code = urls_code.replace(
        "path('<int:enc_id>/', views.editar_trd, name='editar_trd'),",
        "path('<int:enc_id>/', views.editar_trd, name='editar_trd'),\n    path('<int:enc_id>/eliminar/', views.eliminar_trd, name='eliminar_trd'),"
    )
    with open(urls_path, 'w', encoding='utf8') as f:
        f.write(urls_code)

# 3. Modificar inicio.html
with open(template_path, 'r', encoding='utf8') as f:
    template_code = f.read()

if 'eliminar_trd' not in template_code:
    delete_button = """
                              <!-- BOTÓN ELIMINAR TRD (SOLO JEFES Y ADMINS) -->
                              {% if user.profile.rol == 'SUPER' or user.profile.rol == 'JEFE' or user.is_superuser %}
                              <a href="{% url 'trd:eliminar_trd' enc_id=t.id %}" onclick="return confirm('¿Está seguro de eliminar toda esta Tabla de Retención Documental? Esta acción borrará todas sus series, subseries y tipos documentales. ¡No se puede deshacer!');" class="w-12 h-12 bg-slate-100 text-slate-400 rounded-2xl inline-flex items-center justify-center hover:bg-comfaRed hover:text-white transition-all shadow-sm" title="Eliminar Tabla">
                                  <i class="fas fa-trash-alt text-lg"></i>
                              </a>
                              {% endif %}
                              """
    template_code = template_code.replace(
        """<a href="{% url 'trd:exportar_pdf' enc_id=t.id %}" target="_blank" rel="noopener noreferrer" class="w-12 h-12 bg-red-50 border-2 border-red-200 text-comfaRed rounded-2xl inline-flex items-center justify-center hover:bg-comfaRed hover:text-white hover:border-comfaRed transition-all shadow-sm" title="Ver / Descargar PDF oficial">
                                <i class="fas fa-file-pdf"></i>
                            </a>""",
        """<a href="{% url 'trd:exportar_pdf' enc_id=t.id %}" target="_blank" rel="noopener noreferrer" class="w-12 h-12 bg-red-50 border-2 border-red-200 text-comfaRed rounded-2xl inline-flex items-center justify-center hover:bg-comfaRed hover:text-white hover:border-comfaRed transition-all shadow-sm" title="Ver / Descargar PDF oficial">
                                <i class="fas fa-file-pdf"></i>
                            </a>""" + "\n" + delete_button
    )
    with open(template_path, 'w', encoding='utf8') as f:
        f.write(template_code)

print("Botón de eliminar TRD inyectado con éxito.")
