import os

path = "trd/views.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('"oficinas_seleccionadas": oficinas_sel,', '"oficinas_seleccionadas": json.dumps(oficinas_sel),')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
