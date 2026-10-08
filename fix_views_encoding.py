import os

views_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\afiliados\views.py'

with open(views_path, 'r', encoding='utf8') as f:
    code = f.read()

code = code.replace("MÃ³dulo", "Modulo")
code = code.replace("CubÃ­culo", "Cubiculo")

with open(views_path, 'w', encoding='utf8') as f:
    f.write(code)

print("Caracteres extraños eliminados de views.py")
