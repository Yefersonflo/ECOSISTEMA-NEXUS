import os

template_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\templates\trd\editar_trd.html'

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

with open(template_path, 'r', encoding='utf8') as f:
    code = f.read()

# Inyectar el modal justo antes de la etiqueta script de Alpine
if "MODAL EDITAR METADATOS TRD" not in code:
    code = code.replace("<script>\nfunction formTRDData() {", modal_html + "\n<script>\nfunction formTRDData() {")
    with open(template_path, 'w', encoding='utf8') as f:
        f.write(code)
    print("Modal inyectado correctamente.")
else:
    print("El modal ya estaba inyectado.")
