import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'x-data="formTRDData()"' in line:
        print(f"x-data starts at {i}")
    if '+ Agregar Nueva Serie a la TRD' in line:
        print(f"Button is at {i}")
