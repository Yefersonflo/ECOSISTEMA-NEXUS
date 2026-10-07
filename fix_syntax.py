import os
import re

path = "trd/templates/trd/inicio.html"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("stats['items']", "stats.items")
with open(path, "w", encoding="utf-8") as f:
    f.write(c)

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Replace {{ var or var2 }} with {{ var|default:var2 }}
def repl_default(m):
    return "{{" + m.group(1) + "|default:" + m.group(2) + "}}"

c = re.sub(r"\{\{\s*([\w\.]+)\s+or\s+([\w\.]+)\s*\}\}", repl_default, c)

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

print("Fixed syntax in templates")
