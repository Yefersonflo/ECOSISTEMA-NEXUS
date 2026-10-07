import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_table = False
for i, line in enumerate(lines):
    if "modoVistaContenido === 'tabla'" in line:
        in_table = True
    if in_table and ("tipos_directos" in line or "sub_item.tipos" in line or "Tipo Documental" in line):
        print(line.strip())
    if in_table and "</tbody>" in line:
        break
