import os, re

path = "trd/templates/trd/catalogo.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace button click
content = content.replace('type="button" @click="abierto = !abierto"', 'type="button" onclick="document.getElementById(\'ofi-panel-dropdown\').classList.toggle(\'hidden\'); document.getElementById(\'ofi-chevron\').classList.toggle(\'rotate-180\');"')

# Replace chevron icon class
content = content.replace(':class="abierto ? \'rotate-180 text-comfaBlue\' : \'\'"', 'id="ofi-chevron"')

# Replace dropdown panel x-show and x-cloak
content = content.replace('<div x-show="abierto" x-cloak', '<div id="ofi-panel-dropdown" class="hidden absolute left-0 right-0 top-full mt-2 bg-white rounded-2xl shadow-2xl border-2 border-slate-300 p-3 z-50 space-y-2"')
# We also need to remove the class string that follows it because we injected class="hidden ..."
# Let's do it safely
content = re.sub(r'x-transition:enter="[^"]*"', '', content)
content = re.sub(r'x-transition:enter-start="[^"]*"', '', content)
content = re.sub(r'x-transition:enter-end="[^"]*"', '', content)
content = re.sub(r'class="absolute left-0 right-0 top-full mt-2 bg-white rounded-2xl shadow-2xl border-2 border-slate-300 p-3 z-50 space-y-2"', '', content)

# Remove @click.outside from form
content = content.replace('" @click.outside="abierto = false"', '"')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
