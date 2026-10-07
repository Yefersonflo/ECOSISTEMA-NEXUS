import re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# count open and close divs
open_divs = len(re.findall(r'<div\b[^>]*>', content))
close_divs = len(re.findall(r'</div\s*>', content))
print(f"Open divs: {open_divs}, Close divs: {close_divs}")
