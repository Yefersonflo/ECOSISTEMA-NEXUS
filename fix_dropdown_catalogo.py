import os

path = "trd/templates/trd/catalogo.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace @click.outside="abierto = false" with nothing, we'll do it manually if needed, or leave it.
# Actually, let's just make the button toggle very explicitly.
content = content.replace('@click.outside="abierto = false"', '@click.outside="abierto = false" id="oficinas-dropdown-container"')
content = content.replace('@click="abierto = !abierto"', 'onclick="document.getElementById(\'ofi-dropdown-panel\').classList.toggle(\'hidden\')"')
content = content.replace('x-show="abierto"', 'id="ofi-dropdown-panel" class="hidden absolute left-0 right-0 top-full mt-2 bg-white rounded-2xl shadow-2xl border-2 border-slate-300 p-3 z-50 space-y-2"')
# But wait, we need to remove the old class attribute for x-show!
