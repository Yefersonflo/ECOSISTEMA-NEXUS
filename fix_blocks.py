with open('trd/templates/trd/diligenciar.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if '{% block title %}' in line and 'Comfacasanare' in line: continue
    if '{% block header_title %}' in line and 'Diligenciar Nueva' in line: continue
    new_lines.append(line)

with open('trd/templates/trd/diligenciar.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
