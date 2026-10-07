import os

path = "trd/templates/trd/catalogo.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "{{ 'true' if (filtros.texto or filtros.oficinas or filtros.oficina or oficinas_tarjetas|length <= 2) else 'false' }}",
    "{% if filtros.texto or filtros.oficinas or filtros.oficina or oficinas_tarjetas|length <= 2 %}true{% else %}false{% endif %}"
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
