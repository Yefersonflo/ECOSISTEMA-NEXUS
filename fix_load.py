import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

if "{% load trd_extras %}" not in content:
    content = "{% load trd_extras %}\n" + content
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
