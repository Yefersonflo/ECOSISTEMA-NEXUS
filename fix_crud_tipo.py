import os

path = "trd/views_crud.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('nivel="Tipo"', 'nivel="TIPO DOCUMENTAL"')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
