import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace cancel buttons in all modals to also include vanilla JS fallback
cancel_btn_1 = """@click="mostrarModalNuevaSubserieDirecta = false\""""
cancel_btn_1_new = """@click="mostrarModalNuevaSubserieDirecta = false" onclick="this.closest('.fixed').style.display = 'none';\""""
content = content.replace(cancel_btn_1, cancel_btn_1_new)

cancel_btn_2 = """@click="mostrarModalEditar = false\""""
cancel_btn_2_new = """@click="mostrarModalEditar = false" onclick="this.closest('.fixed').style.display = 'none';\""""
content = content.replace(cancel_btn_2, cancel_btn_2_new)

cancel_btn_3 = """@click="mostrarModalNuevoCatalogo = false\""""
cancel_btn_3_new = """@click="mostrarModalNuevoCatalogo = false" onclick="this.closest('.fixed').style.display = 'none';\""""
content = content.replace(cancel_btn_3, cancel_btn_3_new)

cancel_btn_4 = """@click="mostrarModalPreview = false\""""
cancel_btn_4_new = """@click="mostrarModalPreview = false" onclick="this.closest('.fixed').style.display = 'none';\""""
content = content.replace(cancel_btn_4, cancel_btn_4_new)

# Make sure all x-show on modals also have style="display:none;" (already did this)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
