import re

with open('trd/templates/trd/diligenciar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The classes to inline
input_cls = "w-full px-5 py-3.5 bg-white border-2 border-slate-300 rounded-2xl text-sm font-bold text-slate-800 placeholder-slate-400 placeholder:font-normal hover:border-slate-400 focus:border-comfaBlue focus:ring-4 focus:ring-blue-100 outline-none transition-all"
label_cls = "text-xs font-black text-slate-700 uppercase tracking-wider mb-2 flex items-center gap-1.5"

# Remove the {% set ... %} lines
content = re.sub(r'\{%\s*set\s*INPUT\s*=\s*".*?"\s*%\}', '', content)
content = re.sub(r'\{%\s*set\s*LABEL\s*=\s*".*?"\s*%\}', '', content)

# Replace {{ INPUT }} and {{ LABEL }}
content = content.replace('{{ INPUT }}', input_cls)
content = content.replace('{{ LABEL }}', label_cls)

# Also fix the duplicate extends and block content that I accidentally created earlier!
# The file has:
# {% extends 'layout/base.html' %}
# {% load static %}
# ...
# {% block content %}
# {% extends 'layout/base.html' %}
# ...
# {% block content %}

if content.count('{% extends') > 1:
    lines = content.splitlines()
    new_lines = []
    seen_extends = False
    seen_block_content = False
    for line in lines:
        if '{% extends' in line:
            if seen_extends: continue
            seen_extends = True
        if '{% block content %}' in line:
            if seen_block_content: continue
            seen_block_content = True
        new_lines.append(line)
    content = '\n'.join(new_lines)

with open('trd/templates/trd/diligenciar.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed Jinja to Django template syntax")
