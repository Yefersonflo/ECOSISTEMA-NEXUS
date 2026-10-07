import os

path = "trd/templates/trd/catalogo.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("{% url 'trd:exportar_pdf_catalogo' **request.GET %}", "#")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
