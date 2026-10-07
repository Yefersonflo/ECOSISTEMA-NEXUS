import os

template_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\templates\trd\editar_trd.html'

with open(template_path, 'r', encoding='utf8') as f:
    code = f.read()

# 1. Revert x-data
code = code.replace(
    """<div class="max-w-[110rem] mx-auto space-y-8 py-6" x-data="{ ...formTRDData(), showModalMetadatos: false }">""",
    """<div class="max-w-[110rem] mx-auto space-y-8 py-6" x-data="formTRDData()">"""
)

# 2. Add showModalMetadatos to formTRDData()
if "showModalMetadatos:" not in code.split("function formTRDData() {")[1]:
    code = code.replace(
        "function formTRDData() {\n    return {",
        "function formTRDData() {\n    return {\n        showModalMetadatos: false,"
    )

with open(template_path, 'w', encoding='utf8') as f:
    f.write(code)
