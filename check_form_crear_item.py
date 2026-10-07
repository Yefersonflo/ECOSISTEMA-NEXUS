import re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_form = False
for i, line in enumerate(lines):
    if 'action="{% url \'trd:crear_item\'' in line:
        in_form = True
        print(f"crear_item form starts at {i}")
    elif in_form and '</form>' in line:
        print(f"crear_item form ends at {i}")
        in_form = False
        break
