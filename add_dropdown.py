import re

with open("templates/layout/base.html", "r", encoding="utf-8") as f:
    content = f.read()

# Find the TRD link block
trd_link_pattern = r'<a href="{% url \'trd:inicio\' %}".*?<i class="fas fa-file-signature w-8 text-center text-xl text-blue-400"></i>.*?<span class="sidebar-text text-xs uppercase tracking-widest">Módulo TRD</span>.*?</a>'

# Create the new dropdown block using Alpine
dropdown_block = """
<!-- MENU DESPLEGABLE TRD -->
<div x-data="{ open: {% if '/trd/' in request.path %}true{% else %}false{% endif %} }" class="relative">
    <button @click="open = !open" class="w-full flex items-center justify-between p-4 rounded-xl text-white font-bold hover:bg-white/10 transition-colors {% if '/trd/' in request.path %}bg-white/10{% endif %}">
        <div class="flex items-center space-x-4">
            <i class="fas fa-file-signature w-8 text-center text-xl text-blue-400"></i>
            <span class="sidebar-text text-xs uppercase tracking-widest">Módulo TRD</span>
        </div>
        <i class="fas fa-chevron-down text-[10px] sidebar-text transition-transform duration-300" :class="{'rotate-180': open}"></i>
    </button>
    
    <div x-show="open" x-collapse class="pl-14 pr-4 space-y-1 mt-1 sidebar-text overflow-hidden">
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

content = re.sub(trd_link_pattern, dropdown_block, content, flags=re.DOTALL)

with open("templates/layout/base.html", "w", encoding="utf-8") as f:
    f.write(content)
