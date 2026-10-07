import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_table = False
for i, line in enumerate(lines):
    if "modoVistaContenido === 'tabla'" in line and "x-cloak" in line:
        in_table = True
    if in_table:
        print(line.rstrip())
        if "</tbody>" in line:
            break
