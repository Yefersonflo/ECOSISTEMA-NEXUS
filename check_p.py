import re

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

preview = re.search(r'(<div[^>]*mostrarModalPreview.*?)(?=</form>|</div>\s*</div>\s*</div>)', content, re.DOTALL)
if preview:
    print(preview.group(1)[:2000]) # first 2000 chars
else:
    print("Not found")
