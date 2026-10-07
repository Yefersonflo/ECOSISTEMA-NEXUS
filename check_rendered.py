import re

with open("rendered_trd_2.html", "r", encoding="utf-8") as f:
    content = f.read()

directives = re.findall(r"(?:x-show|x-text|x-model|@click|:class|:value|x-if)='([^']+)'", content)
for d in directives:
    if "{" in d or '"' in d:
        print(f"Suspicious single-quoted: {d}")

directives_double = re.findall(r'(?:x-show|x-text|x-model|@click|:class|:value|x-if)="([^"]+)"', content)
for d in directives_double:
    if "{" in d or "'" in d:
        print(f"Suspicious double-quoted: {d}")
