import json

with open("rendered_trd_2.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
directives = re.findall(r"(?:x-show|x-text|x-model|@click|:class|:value|x-if)='([^']+)'", content)
for d in directives:
    if "{" in d or '"' in d:
        print(d.encode('utf-8'))
