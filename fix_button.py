import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Remove x-collapse from the form
content = content.replace("x-collapse", "")
# Fix the button text native
content = content.replace(
    "<span x-text=\"formularioAbierto ? 'Ocultar Formulario' : '+ Agregar Nueva Serie a la TRD'\"></span>",
    "<span x-text=\"formularioAbierto ? 'Ocultar Formulario' : '+ Agregar Nueva Serie a la TRD'\">+ Agregar Nueva Serie a la TRD</span>"
)

# Convert the button to trigger BOTH Alpine and Vanilla JS fallback for the form!
# We will wrap the form in a div id="formTRDContainer"
old_form = """<form method="post" action="{% url 'trd:crear_item' enc_id=enc_id %}"
          x-ref="formularioTRD"
          x-show="formularioAbierto"
          
          x-cloak
          @submit.prevent="enviarFormulario()"
          class="bg-white border-2 border-slate-200 rounded-3xl shadow-lg overflow-hidden relative">"""

new_form = """<form method="post" action="{% url 'trd:crear_item' enc_id=enc_id %}"
          id="formularioTRD"
          x-ref="formularioTRD"
          x-show="formularioAbierto"
          @submit.prevent="enviarFormulario()"
          class="bg-white border-2 border-slate-200 rounded-3xl shadow-lg overflow-hidden relative">"""
content = content.replace(old_form, new_form)

# And fallback the button
old_btn = """<button type="button" @click="formularioAbierto = !formularioAbierto; if (formularioAbierto) { (() => .formularioTRD.scrollIntoView({ behavior: 'smooth' })) }\""""
new_btn = """<button type="button" @click="formularioAbierto = !formularioAbierto; if (formularioAbierto) { (() => .formularioTRD.scrollIntoView({ behavior: 'smooth' })) }" onclick="var f = document.getElementById('formularioTRD'); if(f.style.display==='none'){f.style.display='block';}else{f.style.display='none';}\""""
content = content.replace(old_btn, new_btn)


with open(path, "w", encoding="utf-8") as f:
    f.write(content)
