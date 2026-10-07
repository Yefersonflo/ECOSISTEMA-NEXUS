import re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

script_start = content.find("<script>")
script_end = content.find("</script>")
script_content = content[script_start:script_end]

for i, line in enumerate(script_content.split('\n')):
    if "mostrarModalNuevaVersion" in line:
        print(f"Line {i}: {line.strip()}")
