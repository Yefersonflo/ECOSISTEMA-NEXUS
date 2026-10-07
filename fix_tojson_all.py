import os, re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r"([a-zA-Z0-9_\.]+)\.to_dict\(\)\|tojson", r"\1.to_json|safe", content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
