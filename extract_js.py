import re, json

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

script_start = content.find("<script>") + 8
script_end = content.find("</script>")
js_code = content[script_start:script_end]

# Mock the jinja template tags for parsing
js_code = js_code.replace("{% if arbol_series and arbol_series|length > 0 %}false{% else %}true{% endif %}", "false")
js_code = js_code.replace("{{ catalogo_json|safe }}", '{"series":[]}')
js_code = js_code.replace("{{ encabezado.oficina_productora }}", "JURIDICA")
js_code = re.sub(r"\{% if arbol_series %\}.*?\{% endif %\}", "", js_code, flags=re.DOTALL)
js_code = re.sub(r"\{\{.*?\}\}", "''", js_code)

with open("test_alpine.js", "w", encoding="utf-8") as f:
    f.write(js_code)

