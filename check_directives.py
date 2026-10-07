import re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract all x-text, x-show, x-model, @click, :class, etc.
directives = re.findall(r'(x-show|x-text|x-model|@click|:class|:value|x-if)="([^"]+)"', content)

for d, expr in directives:
    if "mostrarModalEditar" in expr or "formularioAbierto" in expr or "subForm" in expr:
        pass
    else:
        # print some
        print(f"{d} = {expr}")
