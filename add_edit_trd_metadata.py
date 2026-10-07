import os

base_dir = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd'
views_path = os.path.join(base_dir, 'views.py')
urls_path = os.path.join(base_dir, 'urls.py')
template_path = os.path.join(base_dir, 'templates', 'trd', 'editar_trd.html')

# 1. Modificar views.py para agregar la actualización
with open(views_path, 'r', encoding='utf8') as f:
    views_code = f.read()

if 'def actualizar_encabezado_trd(' not in views_code:
    new_view = """
def actualizar_encabezado_trd(request, enc_id):
    if not is_trd_admin(request.user):
        messages.error(request, 'No tienes permisos para editar los metadatos de la Tabla de Retención.')
        return redirect('trd:editar_trd', enc_id=enc_id)
        
    if request.method == 'POST':
        from django.shortcuts import get_object_or_404
        from .models import EncabezadoTRD
        
        try:
            enc = get_object_or_404(EncabezadoTRD, id=enc_id)
            enc.entidad_productora = request.POST.get('entidad_productora', enc.entidad_productora).strip()
            enc.fecha_creacion = request.POST.get('fecha_creacion', enc.fecha_creacion).strip()
            enc.fecha_ajuste = request.POST.get('fecha_ajuste', enc.fecha_ajuste).strip()
            enc.fecha_aprobacion = request.POST.get('fecha_aprobacion', enc.fecha_aprobacion).strip()
            enc.fecha_convalidacion = request.POST.get('fecha_convalidacion', enc.fecha_convalidacion).strip()
            enc.responsable_gestion_documental = request.POST.get('resp_gd', enc.responsable_gestion_documental).strip()
            enc.cargo_responsable_gestion_documental = request.POST.get('cargo_gd', enc.cargo_responsable_gestion_documental).strip()
            enc.responsable_area = request.POST.get('resp_area', enc.responsable_area).strip()
            enc.cargo_responsable_area = request.POST.get('cargo_area', enc.cargo_responsable_area).strip()
            enc.superior_jerarquico = request.POST.get('resp_sup', enc.superior_jerarquico).strip()
            enc.cargo_superior_jerarquico = request.POST.get('cargo_sup', enc.cargo_superior_jerarquico).strip()
            enc.version = request.POST.get('version', enc.version).strip()
            enc.estado = request.POST.get('estado', enc.estado).strip()
            enc.vigencia_ano = request.POST.get('vigencia_ano', enc.vigencia_ano).strip()
            enc.save()
            messages.success(request, '¡Los datos principales de la TRD fueron actualizados con éxito!')
        except Exception as e:
            messages.error(request, f'Error al actualizar TRD: {str(e)}')
            
    return redirect('trd:editar_trd', enc_id=enc_id)
"""
    views_code += new_view
    with open(views_path, 'w', encoding='utf8') as f:
        f.write(views_code)

# 2. Modificar urls.py
with open(urls_path, 'r', encoding='utf8') as f:
    urls_code = f.read()

if 'actualizar_encabezado_trd' not in urls_code:
    urls_code = urls_code.replace(
        "path('<int:enc_id>/eliminar/', views.eliminar_trd, name='eliminar_trd'),",
        "path('<int:enc_id>/eliminar/', views.eliminar_trd, name='eliminar_trd'),\n    path('<int:enc_id>/actualizar_metadatos/', views.actualizar_encabezado_trd, name='actualizar_encabezado_trd'),"
    )
    with open(urls_path, 'w', encoding='utf8') as f:
        f.write(urls_code)

# 3. Modificar editar_trd.html para agregar el botón y el modal
with open(template_path, 'r', encoding='utf8') as f:
    template_code = f.read()

# a. Agregar el botón al lado de la vigencia
btn_html = """
                {% if user.profile.rol == 'SUPER' or user.profile.rol == 'JEFE' or user.is_superuser %}
                <button @click="showModalMetadatos = true" class="px-3 py-1 bg-comfaBlue/10 text-comfaBlue hover:bg-comfaBlue hover:text-white transition-colors border border-comfaBlue/30 rounded-xl text-[10px] font-black uppercase tracking-wider ml-2 cursor-pointer shadow-sm">
                    <i class="fas fa-cog mr-1"></i> Editar Datos
                </button>
                {% endif %}"""

if "showModalMetadatos = true" not in template_code:
    template_code = template_code.replace(
        "{% if encabezado.vigencia_ano %}\n                <span class=\"px-2.5 py-0.5 bg-amber-100 text-amber-800 border border-amber-300 rounded-lg text-[10px] font-black uppercase tracking-wider\">\n                    Vigencia {{ encabezado.vigencia_ano }}\n                </span>\n                {% endif %}",
        "{% if encabezado.vigencia_ano %}\n                <span class=\"px-2.5 py-0.5 bg-amber-100 text-amber-800 border border-amber-300 rounded-lg text-[10px] font-black uppercase tracking-wider\">\n                    Vigencia {{ encabezado.vigencia_ano }}\n                </span>\n                {% endif %}\n" + btn_html
    )

    # b. Inicializar Alpine data
    template_code = template_code.replace("x-data=\"formTRDData()\"", "x-data=\"{ ...formTRDData(), showModalMetadatos: false }\"")

    # c. Agregar el Modal al final de content
    modal_html = """
    <!-- MODAL EDITAR METADATOS TRD -->
    <div x-show="showModalMetadatos" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-comfaBlue/80 backdrop-blur-md" x-cloak>
        <div @click.away="showModalMetadatos = false" class="bg-white w-full max-w-4xl rounded-[3rem] shadow-2xl overflow-y-auto max-h-[90vh]" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 scale-90" x-transition:enter-end="opacity-100 scale-100">
            <div class="bg-comfaBlue p-8 text-white flex justify-between items-center border-b-8 border-comfaYellow sticky top-0 z-10">
                <div>
                    <h3 class="text-xl font-black uppercase tracking-tight">Editar Datos de la Tabla</h3>
                    <p class="text-[10px] font-bold text-comfaYellow uppercase tracking-widest mt-1">{{ encabezado.oficina_productora }}</p>
                </div>
                <button @click="showModalMetadatos = false" type="button" class="text-white/50 hover:text-white transition-colors text-2xl cursor-pointer"><i class="fas fa-times"></i></button>
            </div>
            
            <form method="POST" action="{% url 'trd:actualizar_encabezado_trd' enc_id=enc_id %}" class="p-10 space-y-8">
                {% csrf_token %}
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <!-- DATOS BÁSICOS -->
                    <div class="col-span-1 md:col-span-3 pb-2 border-b border-slate-100">
                        <h4 class="text-xs font-black text-comfaBlue uppercase tracking-widest"><i class="fas fa-info-circle mr-2"></i> Identificación General</h4>
                    </div>
                    
                    <div class="space-y-2 col-span-1 md:col-span-3">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Entidad Productora</label>
                        <input type="text" name="entidad_productora" value="{{ encabezado.entidad_productora }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Versión (Ej: 1.0)</label>
                        <input type="text" name="version" value="{{ encabezado.version }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Año de Vigencia</label>
                        <input type="text" name="vigencia_ano" value="{{ encabezado.vigencia_ano }}" placeholder="Opcional" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Estado</label>
                        <select name="estado" class="w-full bg-white border-2 border-slate-200 rounded-xl px-4 py-4 text-sm font-bold focus:border-comfaBlue outline-none transition-all cursor-pointer">
                            <option value="VIGENTE" {% if encabezado.estado == 'VIGENTE' %}selected{% endif %}>Vigente</option>
                            <option value="EN ELABORACION" {% if encabezado.estado == 'EN ELABORACION' %}selected{% endif %}>En Elaboración</option>
                            <option value="OBSOLETO" {% if encabezado.estado == 'OBSOLETO' %}selected{% endif %}>Obsoleto</option>
                        </select>
                    </div>

                    <!-- FECHAS IMPORTANTES -->
                    <div class="col-span-1 md:col-span-3 pb-2 border-b border-slate-100 mt-4">
                        <h4 class="text-xs font-black text-comfaYellow uppercase tracking-widest"><i class="fas fa-calendar-alt mr-2"></i> Fechas de Registro</h4>
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Creación</label>
                        <input type="text" name="fecha_creacion" value="{{ encabezado.fecha_creacion }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Aprobación (Opcional)</label>
                        <input type="text" name="fecha_aprobacion" value="{{ encabezado.fecha_aprobacion }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Convalidación (Opcional)</label>
                        <input type="text" name="fecha_convalidacion" value="{{ encabezado.fecha_convalidacion }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>

                    <!-- FIRMAS Y RESPONSABLES -->
                    <div class="col-span-1 md:col-span-3 pb-2 border-b border-slate-100 mt-4">
                        <h4 class="text-xs font-black text-slate-800 uppercase tracking-widest"><i class="fas fa-signature mr-2"></i> Firmas y Responsables</h4>
                    </div>
                    <div class="space-y-2 md:col-span-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Responsable Gestión Documental (Ej: Nombre)</label>
                        <input type="text" name="resp_gd" value="{{ encabezado.responsable_gestion_documental }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2 md:col-span-1">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Cargo</label>
                        <input type="text" name="cargo_gd" value="{{ encabezado.cargo_responsable_gestion_documental }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>

                    <div class="space-y-2 md:col-span-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Responsable del Área (Ej: Líder de la Oficina)</label>
                        <input type="text" name="resp_area" value="{{ encabezado.responsable_area }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2 md:col-span-1">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Cargo</label>
                        <input type="text" name="cargo_area" value="{{ encabezado.cargo_responsable_area }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>

                    <div class="space-y-2 md:col-span-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Superior Jerárquico / Aprobador Final</label>
                        <input type="text" name="resp_sup" value="{{ encabezado.superior_jerarquico }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2 md:col-span-1">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Cargo</label>
                        <input type="text" name="cargo_sup" value="{{ encabezado.cargo_superior_jerarquico }}" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                </div>
                
                <button type="submit" class="w-full mt-8 py-5 bg-comfaBlue text-white font-black rounded-2xl shadow-xl hover:bg-comfaRed transition-all uppercase text-[11px] tracking-widest cursor-pointer flex items-center justify-center">
                    Guardar Cambios <i class="fas fa-save ml-3 text-lg"></i>
                </button>
            </form>
        </div>
    </div>
"""
    template_code = template_code.replace("</div>\n{% endblock %}", "\n" + modal_html + "</div>\n{% endblock %}")

    with open(template_path, 'w', encoding='utf8') as f:
        f.write(template_code)

print("Modal de edición de metadatos TRD inyectado con éxito.")
