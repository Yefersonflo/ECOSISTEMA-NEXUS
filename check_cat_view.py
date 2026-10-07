import os

path = "trd/views.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_cat = False
for i, line in enumerate(lines):
    if "def catalogo" in line:
        in_cat = True
    if in_cat:
        print(line.rstrip())
        if "return render" in line:
            break
