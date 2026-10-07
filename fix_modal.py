import os, re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Alpine logic for the Modal Crear Nueva Version with Vanilla JS
# 1. Update the button that opens it
old_open_btn = """<button type="button" @click="mostrarModalNuevaVersion = true"
                    class="px-5 py-4 bg-comfaBlue hover:bg-[#003a6b] text-white rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all shadow-md flex items-center gap-2 cursor-pointer">"""

new_open_btn = """<button type="button" onclick="document.getElementById('modalNuevaVersion').classList.remove('hidden'); document.getElementById('modalNuevaVersion').classList.add('flex');"
                    class="px-5 py-4 bg-comfaBlue hover:bg-[#003a6b] text-white rounded-2xl text-[10px] font-black uppercase tracking-widest transition-all shadow-md flex items-center gap-2 cursor-pointer">"""

content = content.replace(old_open_btn, new_open_btn)

# 2. Update the modal container
old_modal = """<div x-show="mostrarModalNuevaVersion" x-cloak class="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">"""
new_modal = """<div id="modalNuevaVersion" class="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm hidden items-center justify-center p-4">"""
content = content.replace(old_modal, new_modal)

# 3. Update the close buttons
old_close_btn1 = """<button type="button" @click="mostrarModalNuevaVersion = false" class="w-7 h-7 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition-colors cursor-pointer">"""
new_close_btn1 = """<button type="button" onclick="document.getElementById('modalNuevaVersion').classList.add('hidden'); document.getElementById('modalNuevaVersion').classList.remove('flex');" class="w-7 h-7 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition-colors cursor-pointer">"""
content = content.replace(old_close_btn1, new_close_btn1)

old_close_btn2 = """<button type="button" @click="mostrarModalNuevaVersion = false" class="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-xl text-xs font-black uppercase tracking-wider transition-colors cursor-pointer">
                            Cancelar
                        </button>"""
new_close_btn2 = """<button type="button" onclick="document.getElementById('modalNuevaVersion').classList.add('hidden'); document.getElementById('modalNuevaVersion').classList.remove('flex');" class="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-800 rounded-xl text-xs font-black uppercase tracking-wider transition-colors cursor-pointer">
                            Cancelar
                        </button>"""
content = content.replace(old_close_btn2, new_close_btn2)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
