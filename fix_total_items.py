import os

path = "trd/templates/trd/inicio.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("{{ t.total_items }}", "{{ t.items.count }}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
