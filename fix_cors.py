import os

path = "templates/layout/base.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    '<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.13.3/dist/cdn.min.js"></script>',
    '<script defer crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.13.3/dist/cdn.min.js"></script>'
)
content = content.replace(
    '<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js"></script>',
    '<script defer crossorigin="anonymous" src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js"></script>'
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
