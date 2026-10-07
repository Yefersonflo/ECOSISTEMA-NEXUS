import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace x-cloak with style="display: none;" for all modals
content = content.replace('x-show="mostrarModalEditar" x-cloak', 'x-show="mostrarModalEditar" style="display: none;"')
content = content.replace('x-show="mostrarModalNuevaSubserieDirecta" x-cloak', 'x-show="mostrarModalNuevaSubserieDirecta" style="display: none;"')
content = content.replace('x-show="mostrarModalNuevoCatalogo" x-cloak', 'x-show="mostrarModalNuevoCatalogo" style="display: none;"')
content = content.replace('x-show="mostrarModalPreview" x-cloak', 'x-show="mostrarModalPreview" style="display: none;"')

# Ensure we catch any other x-cloak if they are modals
content = content.replace('x-show="erroresValidacion.length > 0" x-cloak', 'x-show="erroresValidacion.length > 0" style="display: none;"')
content = content.replace('x-show="serie_soporte_electronico" x-cloak', 'x-show="serie_soporte_electronico" style="display: none;"')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
