import os
path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_form = False
for i, line in enumerate(lines):
    if 'x-ref="formularioTRD"' in line:
        in_form = True
        print(f"Form starts at {i}")
    if in_form and '</form>' in line:
        print(f"Form ends at {i}")
        # wait there are many forms.
