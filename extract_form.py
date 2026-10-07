import os
import re

base_dir = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web'

# 1. Modificar views.py
views_path = os.path.join(base_dir, 'afiliados', 'views.py')
with open(views_path, 'r', encoding='utf8') as f:
    views_code = f.read()

if 'def crear_registro' not in views_code:
    new_view = """

@login_required
def crear_registro(request):
    cat_activa = request.GET.get('cat', 'TRABAJADOR').upper()
    form = CarpetaForm(initial={'categoria': cat_activa})
    
    if request.method == 'POST':
        if not is_jefe(request.user):
            messages.error(request, 'No tiene permisos para crear nuevos registros.')
            return redirect('gestion_documental')
            
        form = CarpetaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                nueva_carpeta = form.save(commit=False)
                nueva_carpeta.modificado_por = request.user
                
                # Asignación automática de niveles según tipo
                if nueva_carpeta.categoria == 'PATRONAL':
                    for nivel in ['nivel_1', 'nivel_2', 'nivel_3', 'nivel_4', 'nivel_5', 'nivel_6']:
                        if not getattr(nueva_carpeta, nivel):
                            setattr(nueva_carpeta, nivel, 'NA')
                            
                nueva_carpeta.save()
                
                HistorialAuditoria.objects.create(
                    usuario=request.user,
                    accion='CREAR',
                    modulo='ARCHIVO_CENTRAL',
                    detalles=f'Creación de expediente {nueva_carpeta.categoria}: {nueva_carpeta.identificacion} - {nueva_carpeta.nombre}'
                )
                messages.success(request, f'¡Expediente de {nueva_carpeta.categoria} guardado con éxito!')
                return redirect('/gestion-documental/?cat=' + nueva_carpeta.categoria)
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Revisa los campos del formulario.')
            
    return render(request, 'afiliados/crear_registro.html', {'form': form, 'cat_activa': cat_activa})
"""
    with open(views_path, 'a', encoding='utf8') as f:
        f.write(new_view)


# 2. Modificar urls.py
urls_path = os.path.join(base_dir, 'config', 'urls.py')
with open(urls_path, 'r', encoding='utf8') as f:
    urls_code = f.read()

if 'crear_registro' not in urls_code:
    urls_code = urls_code.replace("gestion_documental, panel_reportes", "gestion_documental, crear_registro, panel_reportes")
    urls_code = urls_code.replace(
        "path('gestion-documental/', gestion_documental, name='gestion_documental'),",
        "path('gestion-documental/', gestion_documental, name='gestion_documental'),\n    path('nuevo-registro/', crear_registro, name='crear_registro'),"
    )
    with open(urls_path, 'w', encoding='utf8') as f:
        f.write(urls_code)


# 3. Crear template crear_registro.html
template_path = os.path.join(base_dir, 'templates', 'afiliados', 'crear_registro.html')
template_code = """{% extends 'layout/base.html' %}
{% load widget_tweaks %}

{% block title %}Nuevo Expediente | Nexus{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto py-8">
    <div class="bg-white rounded-[3rem] shadow-2xl overflow-hidden">
        <div class="bg-comfaBlue p-8 text-white flex justify-between items-center border-b-8 border-comfaYellow">
            <div>
                <h3 class="text-3xl font-black uppercase tracking-tight">Nuevo Registro</h3>
                <p class="text-xs font-bold text-comfaYellow uppercase tracking-widest mt-1">
                    {% if cat_activa == 'PATRONAL' %}Expediente Patronal{% else %}Expediente Trabajador{% endif %}
                </p>
            </div>
            <a href="{% url 'gestion_documental' %}" class="text-white/50 hover:text-white transition-colors text-3xl cursor-pointer">
                <i class="fas fa-times-circle"></i>
            </a>
        </div>
        <form method="POST" enctype="multipart/form-data" class="p-10 space-y-6">
            {% csrf_token %}
            
            <div class="grid grid-cols-2 gap-6">
                <!-- Identificación y Nombre -->
                <div class="col-span-2 md:col-span-1 p-4 bg-slate-50 rounded-2xl border border-slate-100">
                    <label class="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Identificación (NIT/CC)</label>
                    {% render_field form.identificacion class="w-full bg-white border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all" placeholder="Ej: 900123456" %}
                    {{ form.identificacion.errors }}
                </div>
                <div class="col-span-2 md:col-span-1 p-4 bg-slate-50 rounded-2xl border border-slate-100">
                    <label class="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Razón Social / Nombre Completo</label>
                    {% render_field form.nombre class="w-full bg-white border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all" placeholder="Nombre completo" %}
                    {{ form.nombre.errors }}
                </div>

                <!-- Categoría -->
                <div class="col-span-2 p-4 bg-slate-50 rounded-2xl border border-slate-100">
                    <label class="text-[10px] font-black text-slate-400 uppercase tracking-widest block mb-2">Tipo de Expediente</label>
                    {% render_field form.categoria class="w-full bg-white border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all" %}
                    {{ form.categoria.errors }}
                </div>

                <!-- Detalles de Ubicación Física -->
                <div class="col-span-2 bg-slate-800 text-white p-6 rounded-3xl mt-4">
                    <h4 class="text-sm font-black uppercase tracking-widest mb-4 text-comfaYellow"><i class="fas fa-map-location-dot mr-2"></i> Ubicación Topográfica</h4>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {% for field in form %}
                            {% if 'nivel_' in field.name or field.name == 'folio' %}
                            <div>
                                <label class="text-[9px] font-bold text-slate-400 uppercase tracking-widest block mb-1">{{ field.label }}</label>
                                {% render_field field class="w-full bg-slate-900 border-2 border-slate-700 rounded-xl px-3 py-2 text-xs font-bold focus:border-comfaYellow outline-none transition-all" %}
                            </div>
                            {% endif %}
                        {% endfor %}
                    </div>
                </div>

                <!-- Archivo Digital -->
                <div class="col-span-2 p-6 bg-comfaBlue/5 rounded-3xl border-2 border-comfaBlue/10">
                    <label class="text-[10px] font-black text-comfaBlue uppercase tracking-widest block mb-2"><i class="fas fa-file-pdf mr-2"></i> Archivo Digital (PDF)</label>
                    {% render_field form.archivo_digital class="w-full text-sm font-bold text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-black file:bg-comfaBlue file:text-white hover:file:bg-comfaRed transition-all" %}
                </div>
            </div>
            <button type="submit" class="w-full py-5 bg-comfaBlue text-white font-black rounded-2xl shadow-xl hover:bg-comfaRed transition-all uppercase text-sm tracking-widest cursor-pointer mt-8">
                Guardar Expediente <i class="fas fa-save ml-2"></i>
            </button>
        </form>
    </div>
</div>
{% endblock %}
"""
with open(template_path, 'w', encoding='utf8') as f:
    f.write(template_code)

# 4. Modificar base.html (añadir enlaces al menu)
base_path = os.path.join(base_dir, 'templates', 'layout', 'base.html')
with open(base_path, 'r', encoding='utf8') as f:
    base_code = f.read()

menu_trabajador = """                    <a href="{% url 'crear_registro' %}?cat=TRABAJADOR" class="block py-2 text-[10px] font-bold text-slate-300 hover:text-comfaYellow transition-colors {% if '/nuevo-registro/' in request.path and request.GET.cat != 'PATRONAL' %}text-comfaYellow{% endif %} uppercase tracking-wider">
                        <i class="fas fa-user-plus mr-2 opacity-50"></i> Nuevo Trabajador
                    </a>
                    <a href="{% url 'crear_registro' %}?cat=PATRONAL" class="block py-2 text-[10px] font-bold text-slate-300 hover:text-comfaYellow transition-colors {% if '/nuevo-registro/' in request.path and request.GET.cat == 'PATRONAL' %}text-comfaYellow{% endif %} uppercase tracking-wider">
                        <i class="fas fa-building-user mr-2 opacity-50"></i> Nuevo Patronal
                    </a>"""

if "Nuevo Trabajador" not in base_code:
    # insert before <a href="{% url 'gestion_documental' %}" inside archivo-submenu
    base_code = base_code.replace(
        """<div id="archivo-submenu" class="hidden pl-14 pr-4 space-y-1 mt-1 sidebar-text transition-all">
                    <a href="{% url 'gestion_documental' %}""",
        f"""<div id="archivo-submenu" class="hidden pl-14 pr-4 space-y-1 mt-1 sidebar-text transition-all">
{menu_trabajador}
                    <a href="{{% url 'gestion_documental' %}}"""
    )
    with open(base_path, 'w', encoding='utf8') as f:
        f.write(base_code)

print("Separación completada.")
