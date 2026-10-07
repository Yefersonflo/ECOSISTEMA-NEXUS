import re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# find script tag
script_start = content.find("<script>")
script_end = content.find("</script>")
script_content = content[script_start:script_end]

for line in script_content.split('\n'):
    if "{{" in line or "{%" in line:
        print(line)
