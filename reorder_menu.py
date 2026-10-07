import os
import re

base_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\templates\layout\base.html'

with open(base_path, 'r', encoding='utf8') as f:
    content = f.read()

# El bloque a buscar
submenu_pattern = r'(<div id="trd-submenu"[^>]*>)\s*(<a href="\{% url \'trd:inicio\' %\}"[^>]*>.*?</a>)\s*(<a href="\{% url \'trd:oficinas\' %\}"[^>]*>.*?</a>)\s*(<a href="\{% url \'trd:catalogo\' %\}"[^>]*>.*?</a>)\s*(<a href="\{% url \'trd:diligenciar\' %\}"[^>]*>.*?</a>)\s*</div>'

match = re.search(submenu_pattern, content, flags=re.DOTALL)
if match:
    # 1: container div, 2: inicio, 3: oficinas, 4: catalogo, 5: nueva tabla
    new_submenu = f"{match.group(1)}\n        {match.group(2)}\n        {match.group(5)}\n        {match.group(3)}\n        {match.group(4)}\n    </div>"
    content = content.replace(match.group(0), new_submenu)
    with open(base_path, 'w', encoding='utf8') as f:
        f.write(content)
    print("Menú TRD reordenado con éxito.")
else:
    print("No se encontró el patrón del menú.")
