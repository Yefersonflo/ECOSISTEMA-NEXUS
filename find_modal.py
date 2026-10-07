import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Modal Crear Nueva Versión de TRD' in line:
        print(f"Modal is at line {i}: {line.strip()}")
