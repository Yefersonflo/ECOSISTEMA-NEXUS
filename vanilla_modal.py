import os
import re

template_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\templates\trd\editar_trd.html'

with open(template_path, 'r', encoding='utf8') as f:
    code = f.read()

# 1. Separar el botón del contexto x-data principal y crearle uno propio al botón y al modal
code = code.replace(
    """<button @click="showModalMetadatos = true" """,
    """<button onclick="document.getElementById('modal-metadatos-trd').classList.remove('hidden');" """
)

code = code.replace(
    """<div x-show="showModalMetadatos" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-comfaBlue/80 backdrop-blur-md" x-cloak>""",
    """<div id="modal-metadatos-trd" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-comfaBlue/80 backdrop-blur-md hidden" style="z-index: 9999;">"""
)

code = code.replace(
    """<div @click.away="showModalMetadatos = false" class="bg-white w-full max-w-4xl rounded-[3rem] shadow-2xl overflow-y-auto max-h-[90vh]" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 scale-90" x-transition:enter-end="opacity-100 scale-100">""",
    """<div class="bg-white w-full max-w-4xl rounded-[3rem] shadow-2xl overflow-y-auto max-h-[90vh]">"""
)

code = code.replace(
    """<button @click="showModalMetadatos = false" type="button" class="text-white/50 hover:text-white transition-colors text-2xl cursor-pointer">""",
    """<button onclick="document.getElementById('modal-metadatos-trd').classList.add('hidden');" type="button" class="text-white/50 hover:text-white transition-colors text-2xl cursor-pointer">"""
)

# 2. Quitar showModalMetadatos de formTRDData
code = code.replace("        showModalMetadatos: false,\n", "")

with open(template_path, 'w', encoding='utf8') as f:
    f.write(code)

print("Modal convertido a Vanilla JS independiente.")
