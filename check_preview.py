import re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

preview_modal = re.search(r'(<div[^>]*x-show="mostrarModalPreview".*?<!-- Fin Modal Preview -->)', content, re.DOTALL)
if preview_modal:
    print(preview_modal.group(1))
else:
    print("Not found with that regex.")
