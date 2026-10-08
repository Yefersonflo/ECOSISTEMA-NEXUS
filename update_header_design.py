import os

template_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\templates\trd\editar_trd.html'

with open(template_path, 'r', encoding='utf8') as f:
    code = f.read()

old_html = """<div class="flex flex-col md:flex-row items-start md:items-center justify-between border-b-2 border-slate-200 px-8 py-5 gap-4 bg-slate-50/50">
            <div class="flex items-center gap-3">
                <i class="fas fa-layer-group text-comfaBlue text-xl"></i>
                <div>
                    <h3 class="text-xs font-black text-comfaBlue uppercase tracking-widest flex items-center gap-2">
                        Contenido de la Tabla de Retención
                    </h3>
                    <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wider">
                        <span x-show="modoVistaContenido === 'acordeon'">Estructura interactiva: haz clic sobre cualquier serie o subserie para desplegar</span>
                        <span x-show="modoVistaContenido === 'tabla'">Vista previa oficial estructurada tipo matriz documental</span>
                    </p>
                </div>
            </div>
            
            <div class="flex flex-wrap items-center gap-3 w-full md:w-auto justify-between md:justify-end">
                <!-- Selector de Vista (Acordeón vs Vista Previa Tabla) -->
                <div class="inline-flex p-1 bg-slate-200/90 rounded-2xl gap-1 shadow-inner">
                    <button type="button" @click="modoVistaContenido = 'acordeon'"
                            :class="modoVistaContenido === 'acordeon' ? 'bg-white text-comfaBlue shadow-xs font-black' : 'text-slate-600 hover:text-slate-900 font-bold'"
                            class="px-3.5 py-1.5 rounded-xl text-xs uppercase tracking-wider transition-all flex items-center gap-1.5 cursor-pointer">
                        <i class="fas fa-layer-group"></i>
                        <span>Contenido</span>
                    </button>
                    <button type="button" @click="modoVistaContenido = 'tabla'"
                            :class="modoVistaContenido === 'tabla' ? 'bg-comfaBlue text-white shadow-xs font-black' : 'text-slate-600 hover:text-slate-900 font-bold'"
                            class="px-3.5 py-1.5 rounded-xl text-xs uppercase tracking-wider transition-all flex items-center gap-1.5 cursor-pointer">
                        <i class="fas fa-table-list"></i>
                        <span>Vista Previa (Tabla)</span>
                    </button>
                </div>

                <span class="px-2.5 py-1.5 bg-indigo-50 border border-indigo-200 text-indigo-900 rounded-xl text-[10px] font-black uppercase">
                    {{ arbol_series|length }} Series &middot; {{ items|length }} registros
                </span>
            </div>
        </div>"""

new_html = """<div class="flex flex-col md:flex-row items-start md:items-center justify-between border-b-4 border-comfaYellow px-8 py-5 gap-4 bg-gradient-to-r from-comfaBlue to-[#003a6b]">
            <div class="flex items-center gap-4">
                <div class="w-11 h-11 rounded-xl bg-white/10 border border-white/20 flex items-center justify-center text-comfaYellow shrink-0 shadow-inner">
                    <i class="fas fa-layer-group text-xl"></i>
                </div>
                <div>
                    <h3 class="text-xs font-black text-white uppercase tracking-widest flex items-center gap-2">
                        Contenido de la Tabla de Retención
                    </h3>
                    <p class="text-[10px] text-blue-100 font-bold uppercase tracking-wider mt-0.5 opacity-90">
                        <span x-show="modoVistaContenido === 'acordeon'">Estructura interactiva: haz clic sobre cualquier serie o subserie para desplegar</span>
                        <span x-show="modoVistaContenido === 'tabla'">Vista previa oficial estructurada tipo matriz documental</span>
                    </p>
                </div>
            </div>
            
            <div class="flex flex-wrap items-center gap-3 w-full md:w-auto justify-between md:justify-end">
                <!-- Selector de Vista (Acordeón vs Vista Previa Tabla) -->
                <div class="inline-flex p-1 bg-white/10 rounded-2xl gap-1 shadow-inner backdrop-blur-sm border border-white/10">
                    <button type="button" @click="modoVistaContenido = 'acordeon'"
                            :class="modoVistaContenido === 'acordeon' ? 'bg-comfaYellow text-slate-900 shadow-md font-black' : 'text-white/80 hover:text-white font-bold'"
                            class="px-4 py-1.5 rounded-xl text-xs uppercase tracking-wider transition-all flex items-center gap-1.5 cursor-pointer">
                        <i class="fas fa-layer-group"></i>
                        <span>Contenido</span>
                    </button>
                    <button type="button" @click="modoVistaContenido = 'tabla'"
                            :class="modoVistaContenido === 'tabla' ? 'bg-comfaYellow text-slate-900 shadow-md font-black' : 'text-white/80 hover:text-white font-bold'"
                            class="px-4 py-1.5 rounded-xl text-xs uppercase tracking-wider transition-all flex items-center gap-1.5 cursor-pointer">
                        <i class="fas fa-table-list"></i>
                        <span>Vista Previa</span>
                    </button>
                </div>

                <span class="px-3 py-1.5 bg-comfaYellow/20 border border-comfaYellow text-comfaYellow rounded-xl text-[10px] font-black uppercase shadow-sm">
                    {{ arbol_series|length }} Series &middot; {{ items|length }} registros
                </span>
            </div>
        </div>"""

if old_html in code:
    code = code.replace(old_html, new_html)
    with open(template_path, 'w', encoding='utf8') as f:
        f.write(code)
    print("Diseño del header de contenido de TRD actualizado con éxito.")
else:
    print("No se encontró el HTML exacto. Puede haber problemas de indentación.")
