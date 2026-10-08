import os

template_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\templates\trd\editar_trd.html'

with open(template_path, 'r', encoding='utf8') as f:
    code = f.read()

# 1. Serie Acordeon
code = code.replace(
    """<span class="px-3 py-1.5 bg-white border-2 border-slate-300 rounded-xl text-xs font-black text-comfaBlue shadow-sm shrink-0">
                            {{ nodo.serie.codigo }}
                        </span>""",
    """<span class="px-3 py-1.5 bg-comfaBlue border-2 border-comfaBlue rounded-xl text-xs font-black text-white shadow-sm shrink-0">
                            {{ nodo.serie.codigo }}
                        </span>"""
)

# 2. Subserie Acordeon
code = code.replace(
    """<span class="px-2.5 py-1 bg-white border-2 border-slate-300 text-comfaBlue font-mono font-black text-xs rounded-xl shadow-2xs shrink-0">
                                            {{ sub_item.subserie.codigo }}
                                        </span>""",
    """<span class="px-2.5 py-1 bg-comfaYellow border-2 border-yellow-500 text-slate-900 font-mono font-black text-xs rounded-xl shadow-2xs shrink-0">
                                            {{ sub_item.subserie.codigo }}
                                        </span>"""
)

# 3. Serie Tabla
code = code.replace(
    """<span class="px-2 py-0.5 bg-white border border-blue-300 rounded-md shadow-2xs">{{ nodo.serie.codigo }}</span>""",
    """<span class="px-2 py-0.5 bg-comfaBlue text-white border border-blue-900 rounded-md shadow-2xs">{{ nodo.serie.codigo }}</span>"""
)

# 4. Subserie Tabla
code = code.replace(
    """<span class="px-2 py-0.5 bg-indigo-50 border border-indigo-200 rounded text-[11px]">{{ sub_item.subserie.codigo }}</span>""",
    """<span class="px-2 py-0.5 bg-comfaYellow font-black text-slate-900 border border-yellow-500 rounded text-[11px]">{{ sub_item.subserie.codigo }}</span>"""
)

with open(template_path, 'w', encoding='utf8') as f:
    f.write(code)

print("Diseño de los códigos de serie y subserie actualizado.")
