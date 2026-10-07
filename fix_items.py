import os, re

tpl_dir = "trd/templates/trd"
for file in os.listdir(tpl_dir):
    if file.endswith(".html"):
        path = os.path.join(tpl_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.replace(".items()", ".items")
        content = content.replace(".keys()", ".keys")
        content = content.replace(".values()", ".values")

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
