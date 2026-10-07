import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_table = False
has_tipos = False
for i, line in enumerate(lines):
    if "modoVistaContenido === 'tabla'" in line:
        in_table = True
    if in_table and ("tipos_directos" in line or "sub_item.tipos" in line):
        has_tipos = True
    if in_table and "</tbody>" in line:
        break

print("Tiene tipos en vista previa?", has_tipos)
