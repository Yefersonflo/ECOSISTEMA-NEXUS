import os
import re

template_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\templates\trd\editar_trd.html'

with open(template_path, 'r', encoding='utf8') as f:
    code = f.read()

form_pattern = re.compile(r'(<form[^>]+method=["\']post["\'][^>]*>)', re.IGNORECASE)

def insert_csrf(match):
    form_tag = match.group(1)
    return form_tag + '\n{% csrf_token %}'

# Remove existing tokens to avoid duplicates
code = re.sub(r'{%\s*csrf_token\s*%}', '', code)
code = form_pattern.sub(insert_csrf, code)

with open(template_path, 'w', encoding='utf8') as f:
    f.write(code)

print("Tokens CSRF inyectados en todos los formularios.")
