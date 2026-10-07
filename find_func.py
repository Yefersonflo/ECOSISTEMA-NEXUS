import os
import ast

found = False
for root, dirs, files in os.walk('trd'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                if 'def agrupar_items_jerarquia' in file.read():
                    print(f"Found in {path}")
                    found = True
                    break
    if found: break
