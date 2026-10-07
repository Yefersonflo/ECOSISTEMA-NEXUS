import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

x_btn_1 = """@click="mostrarModalNuevaSubserieDirecta = false" class="w-7 h-7"""
x_btn_1_new = """@click="mostrarModalNuevaSubserieDirecta = false" onclick="this.closest('.fixed').style.display = 'none';" class="w-7 h-7"""
content = content.replace(x_btn_1, x_btn_1_new)

x_btn_2 = """@click="mostrarModalEditar = false" class="w-7 h-7"""
x_btn_2_new = """@click="mostrarModalEditar = false" onclick="this.closest('.fixed').style.display = 'none';" class="w-7 h-7"""
content = content.replace(x_btn_2, x_btn_2_new)

x_btn_3 = """@click="mostrarModalNuevoCatalogo = false" class="w-7 h-7"""
x_btn_3_new = """@click="mostrarModalNuevoCatalogo = false" onclick="this.closest('.fixed').style.display = 'none';" class="w-7 h-7"""
content = content.replace(x_btn_3, x_btn_3_new)

x_btn_4 = """@click="mostrarModalPreview = false" class="w-7 h-7"""
x_btn_4_new = """@click="mostrarModalPreview = false" onclick="this.closest('.fixed').style.display = 'none';" class="w-7 h-7"""
content = content.replace(x_btn_4, x_btn_4_new)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
