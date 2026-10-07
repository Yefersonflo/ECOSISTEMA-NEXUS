import os, re

tpl_dir = "trd/templates/trd"
for file in os.listdir(tpl_dir):
    if file.endswith(".html"):
        path = os.path.join(tpl_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace {{ var or 'string' }} -> {{ var|default:'string' }}
        def repl(m):
            v1 = m.group(1).strip()
            v2 = m.group(2).strip()
            return "{{" + v1 + "|default:" + v2 + "}}"

        content = re.sub(r"\{\{\s*([a-zA-Z0-9_\.]+)\s+or\s+('[^']+'|\"[^\"]+\"|[a-zA-Z0-9_\.]+)\s*\}\}", repl, content)
        
        # Also replace "or '-' "
        # Also replace "{{ t.estado or 'VIGENTE' }}"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
