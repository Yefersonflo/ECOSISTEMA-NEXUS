import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_table = False
table_content = []
for i, line in enumerate(lines):
    if "modoVistaContenido === 'tabla'" in line:
        in_table = True
    if in_table:
        table_content.append(line)
        if "</tbody>" in line:
            break

for line in table_content:
    if "tipo" in line.lower():
        print(line.strip().encode('utf-8'))
