import os

template_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\templates\afiliados\mapa_visual.html'

with open(template_path, 'r', encoding='utf8') as f:
    code = f.read()

code = code.replace("Mód</p>", "MOD</p>")
code = code.replace("Módulo", "Modulo")
code = code.replace("módulo", "modulo")
code = code.replace("Navegación", "Navegacion")
code = code.replace("SELECCIÓN", "SELECCION")
code = code.replace("BOTÓN", "BOTON")

with open(template_path, 'w', encoding='utf8') as f:
    f.write(code)

print("Tildes eliminadas del mapa_visual.html")
