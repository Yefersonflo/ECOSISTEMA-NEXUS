import os

path = "trd/utils/catalogo_ccd.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("import oficinas", "from trd.utils import oficinas")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
