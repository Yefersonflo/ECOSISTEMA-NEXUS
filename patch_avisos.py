import os, re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Add {% load trd_extras %} at the top after {% extends ... %}
content = re.sub(r'(\{% extends [^\}]+\}%\})', r'\1\n{% load trd_extras %}', content, count=1)

# Replace the avisos logic
old_avisos = """{% if avisos.get(nodo.serie.id) %}
                                {% for aviso in avisos[nodo.serie.id] %}
                                <p class="text-[10px] font-bold text-amber-700 mt-0.5"><i class="fas fa-triangle-exclamation mr-1"></i>{{ aviso }}</p>
                                {% endfor %}
                            {% endif %}"""

new_avisos = """{% with avisos_serie=avisos|get_item:nodo.serie.id %}
                                {% if avisos_serie %}
                                    {% for aviso in avisos_serie %}
                                    <p class="text-[10px] font-bold text-amber-700 mt-0.5"><i class="fas fa-triangle-exclamation mr-1"></i>{{ aviso }}</p>
                                    {% endfor %}
                                {% endif %}
                            {% endwith %}"""

content = content.replace(old_avisos, new_avisos)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
