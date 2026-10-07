import os
import re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# I will find the first <div x-data="formTRDData()"> and see if the modal is inside it.
# Instead of full parse, let's just count open/close tags for divs from line 15 to line 1610.

lines = content.split('\n')
div_depth = 0
inside_xdata = False
for i, line in enumerate(lines):
    if i >= 15:
        div_depth += line.count('<div')
        div_depth -= line.count('</div')
        
        if i == 1610:
            print(f"At Modal (line 1610), div_depth is {div_depth}")
        if div_depth == 0:
            print(f"x-data div closes at line {i}")
            break
