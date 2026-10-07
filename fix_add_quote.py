import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("{{ nodo.subseries|length|add:'1' }}", '{{ nodo.subseries|length|add:"1" }}')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
