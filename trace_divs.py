import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

div_count = 0
for i, line in enumerate(lines):
    if 'x-data="formTRDData()"' in line:
        print(f"Line {i}: {line.strip()}")
        # We start counting from this line
        break
