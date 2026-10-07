import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_preview = False
for i, line in enumerate(lines):
    if 'mostrarModalPreview' in line and '<div' in line:
        in_preview = True
    if in_preview:
        print(line.rstrip())
        if 'Crear Nueva Versión' in line: # Stop when we reach next modal
            break
