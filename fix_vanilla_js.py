import re

with open("templates/layout/base.html", "r", encoding="utf-8") as f:
    content = f.read()

dropdown_block = """
<!-- MENU DESPLEGABLE TRD -->
<div class="relative w-full">
    <button type="button" onclick="document.getElementById('trd-submenu').classList.toggle('hidden'); document.getElementById('trd-chevron').classList.toggle('rotate-180');" class="w-full flex items-center justify-between p-4 rounded-xl text-white font-bold hover:bg-white/10 transition-colors {% if '/trd/' in request.path %}bg-white/10{% endif %}">
        <div class="flex items-center space-x-4 pointer-events-none">
            <i class="fas fa-file-signature w-8 text-center text-xl text-blue-400"></i>
            <span class="sidebar-text text-xs uppercase tracking-widest">Módulo TRD</span>
        </div>
        <i id="trd-chevron" class="fas fa-chevron-down text-[10px] sidebar-text transition-transform duration-300 pointer-events-none"></i>
    </button>
    
    <div id="trd-submenu" class="hidden pl-14 pr-4 space-y-1 mt-1 sidebar-text transition-all">
        <a href="{% url 'trd:inicio' %}" class="block py-2 text-[10px] font-bold text-slate-300 hover:text-comfaYellow transition-colors {% if request.resolver_match.url_name == 'inicio' %}text-comfaYellow{% endif %} uppercase tracking-wider">
            <i class="fas fa-chart-pie mr-2 opacity-50"></i> Panel Principal
        </a>
        <a href="{% url 'trd:oficinas' %}" class="block py-2 text-[10px] font-bold text-slate-300 hover:text-comfaYellow transition-colors {% if request.resolver_match.url_name == 'oficinas' %}text-comfaYellow{% endif %} uppercase tracking-wider">
            <i class="fas fa-building mr-2 opacity-50"></i> Oficinas
        </a>
        <a href="{% url 'trd:catalogo' %}" class="block py-2 text-[10px] font-bold text-slate-300 hover:text-comfaYellow transition-colors {% if request.resolver_match.url_name == 'catalogo' %}text-comfaYellow{% endif %} uppercase tracking-wider">
            <i class="fas fa-book mr-2 opacity-50"></i> Catálogo CCD
        </a>
        <a href="{% url 'trd:diligenciar' %}" class="block py-2 text-[10px] font-bold text-slate-300 hover:text-comfaYellow transition-colors {% if request.resolver_match.url_name == 'diligenciar' %}text-comfaYellow{% endif %} uppercase tracking-wider">
            <i class="fas fa-plus-circle mr-2 opacity-50"></i> Nueva Tabla
        </a>
    </div>
</div>
"""

pattern = r"<!-- MENU DESPLEGABLE TRD -->.*?</div>\s*</div>"
content = re.sub(pattern, dropdown_block, content, flags=re.DOTALL)

with open("templates/layout/base.html", "w", encoding="utf-8") as f:
    f.write(content)
