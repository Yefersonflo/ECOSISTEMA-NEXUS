import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_table = False
for i, line in enumerate(lines):
    if "<!-- TIPOS DOCUMENTALES DE LA SUBSERIE -->" in line:
        in_table = True
    if in_table:
        print(line.rstrip())
        if "<!-- ================= TIPOS DIRECTOS DE SERIE SIMPLE ================= -->" in line:
            break
