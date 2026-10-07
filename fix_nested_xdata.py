import os, re

path = "trd/templates/trd/catalogo.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace <form method="get" x-data
form_start = """<form method="get" x-data="{
        abierto: false,
        busqueda: '{{ filtros.texto|escapejs }}',
        seleccionadas: {{ oficinas_seleccionadas|safe }},
        marcarTodas() {
            this.seleccionadas = [{% for o in oficinas %}'{{ o.nombre|escapejs }}'{% if not forloop.last %},{% endif %}{% endfor %}];
        },
        limpiarTodas() {
            this.seleccionadas = [];
        }
    }" @click.outside="abierto = false"
"""
content = re.sub(r'<form method="get" x-data', form_start, content, count=1)

# Remove the inner x-data block from the div
inner_xdata_pattern = r'x-data="\{\s*abierto: false,\s*busqueda: \'\',\s*seleccionadas: \{\{ oficinas_seleccionadas \| safe \}\},\s*marcarTodas\(\) \{\s*this\.seleccionadas = \[\{% for o in oficinas %\}\'\{\{ o\.nombre \}\}\',\{% endfor %\}\];\s*\},\s*limpiarTodas\(\) \{\s*this\.seleccionadas = \[\];\s*\}\s*\}" @click\.outside="abierto = false"'
content = re.sub(inner_xdata_pattern, '', content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
