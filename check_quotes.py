import re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

directives = re.findall(r"(?:x-show|x-text|x-model|@click|:class|:value|x-if)='([^']+)'", content)
for d in directives:
    if "'" in d:
        print(f"Single quote inside single quote: {d}")

directives_double = re.findall(r'(?:x-show|x-text|x-model|@click|:class|:value|x-if)="([^"]+)"', content)
for d in directives_double:
    if '"' in d:
        print(f"Double quote inside double quote: {d}")
