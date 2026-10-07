import os

path = "trd/templates/trd/catalogo.html"
if os.path.exists(path):
    print("catalogo.html found. Showing table:")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if "{% for" in line:
            print(f"L{i}: {line.strip()}")
else:
    print("catalogo.html NOT FOUND!")
