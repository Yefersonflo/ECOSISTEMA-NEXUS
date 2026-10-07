import re

with open("templates/layout/base.html", "r", encoding="utf-8") as f:
    content = f.read()

# Change x-data="{ open: true }" to "{ open: false }" so it's always closed by default
content = re.sub(r'x-data="\{ open: \{% if \'/trd/\' in request.path %\}true\{% else %\}false\{% endif %\} \}"', 'x-data="{ open: false }"', content)

with open("templates/layout/base.html", "w", encoding="utf-8") as f:
    f.write(content)
