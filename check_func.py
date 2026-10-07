import os

path = "trd/views.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_func = False
for i, line in enumerate(lines):
    if "def agrupar_items_jerarquia" in line:
        in_func = True
    if in_func:
        print(line.rstrip())
        if "return series" in line:
            break
