import re

file_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\templates\layout\base.html'
with open(file_path, 'r', encoding='utf8') as f:
    html = f.read()

old_archivo_central = """            <!-- ARCHIVO CENTRAL -->
            <div class="pt-4 pb-2 text-center group-hover:text-left transition-all">
                <div class="h-px bg-white/10 w-full group-hover:hidden"></div>
                <p class="sidebar-text text-[9px] font-black text-slate-400 uppercase tracking-[0.3em] px-4">Archivo Central</p>
            </div>
            <a href="{% url 'gestion_documental' %}" class="flex items-center space-x-4 p-4 rounded-xl text-white font-bold hover:bg-white/10 {% if '/gestion-documental/' in request.path %}nav-item-active{% endif %}">   
                <i class="fas fa-boxes-stacked w-8 text-center text-xl text-comfaYellow"></i>
                <span class="sidebar-text text-xs uppercase tracking-widest">Gestión Documental</span>     
            </a>
            <a href="{% url 'mapa_visual' %}" class="flex items-center space-x-4 p-4 rounded-xl text-white font-bold hover:bg-white/10 {% if '/mapa-visual/' in request.path %}nav-item-active{% endif %}">
                <i class="fas fa-warehouse w-8 text-center text-xl text-orange-400"></i>
                <span class="sidebar-text text-xs uppercase tracking-widest">Visor de Bodega</span>
            </a>"""

new_archivo_central = """            <!-- ARCHIVO CENTRAL ACORDEON -->
            <div class="pt-4 pb-2 text-center group-hover:text-left transition-all">
                <div class="h-px bg-white/10 w-full group-hover:hidden"></div>
                <p class="sidebar-text text-[9px] font-black text-slate-400 uppercase tracking-[0.3em] px-4">Archivo Físico</p>
            </div>
            <div class="relative w-full">
                <button type="button" onclick="document.getElementById('archivo-submenu').classList.toggle('hidden'); document.getElementById('archivo-chevron').classList.toggle('rotate-180');" class="w-full flex items-center justify-between p-4 rounded-xl text-white font-bold hover:bg-white/10 transition-colors {% if '/gestion-documental/' in request.path or '/mapa-visual/' in request.path or '/reportes-registros/' in request.path %}bg-white/10{% endif %}">
                    <div class="flex items-center space-x-4 pointer-events-none">
                        <i class="fas fa-boxes-stacked w-8 text-center text-xl text-comfaYellow"></i>
                        <span class="sidebar-text text-xs uppercase tracking-widest">Gestión Documental</span>
                    </div>
                    <i id="archivo-chevron" class="fas fa-chevron-down text-[10px] sidebar-text transition-transform duration-300 pointer-events-none"></i>
                </button>
                
                <div id="archivo-submenu" class="hidden pl-14 pr-4 space-y-1 mt-1 sidebar-text transition-all">
                    <a href="{% url 'gestion_documental' %}" class="block py-2 text-[10px] font-bold text-slate-300 hover:text-comfaYellow transition-colors {% if '/gestion-documental/' in request.path %}text-comfaYellow{% endif %} uppercase tracking-wider">
                        <i class="fas fa-search mr-2 opacity-50"></i> Explorador
                    </a>
                    <a href="{% url 'mapa_visual' %}" class="block py-2 text-[10px] font-bold text-slate-300 hover:text-comfaYellow transition-colors {% if '/mapa-visual/' in request.path %}text-comfaYellow{% endif %} uppercase tracking-wider">
                        <i class="fas fa-warehouse mr-2 opacity-50"></i> Visor de Bodega
                    </a>
                    {% if user.profile.rol == 'SUPER' or user.profile.rol == 'JEFE' or user.is_superuser %}
                    <a href="{% url 'panel_reportes' %}" class="block py-2 text-[10px] font-bold text-slate-300 hover:text-comfaYellow transition-colors {% if '/reportes-registros/' in request.path %}text-comfaYellow{% endif %} uppercase tracking-wider">
                        <i class="fas fa-file-excel mr-2 opacity-50"></i> Reportes Excel
                    </a>
                    {% endif %}
                </div>
            </div>"""

old_reportes = """            <a href="{% url 'panel_reportes' %}" class="flex items-center space-x-3 p-3 rounded-xl text-white font-bold hover:bg-white/10 {% if '/reportes-registros/' in request.path %}nav-item-active{% endif %}">       
                <i class="fas fa-file-excel w-7 text-center text-lg text-green-400"></i>
                <span class="sidebar-text text-xs uppercase tracking-widest">Generador Reportes</span>      
            </a>"""

if old_archivo_central in html:
    html = html.replace(old_archivo_central, new_archivo_central)
    html = html.replace(old_reportes, "")
    
    # Check if there are double newlines created
    html = html.replace("\n\n\n", "\n\n")

    with open(file_path, 'w', encoding='utf8') as f:
        f.write(html)
    print("Reemplazo exitoso.")
else:
    print("No se encontró el bloque a reemplazar. Puede que ya se haya modificado.")
