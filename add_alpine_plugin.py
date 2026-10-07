import re

with open("templates/layout/base.html", "r", encoding="utf-8") as f:
    content = f.read()

# Add collapse plugin before alpinejs
alpine_script = '<script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>'
alpine_with_plugin = '<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>\n    ' + alpine_script

content = content.replace(alpine_script, alpine_with_plugin)

with open("templates/layout/base.html", "w", encoding="utf-8") as f:
    f.write(content)
