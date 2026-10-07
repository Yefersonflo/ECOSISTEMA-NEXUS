import os

path = "templates/layout/base.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Alpine CDNs
old_cdn1 = '<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>'
old_cdn2 = '<script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>'

new_cdn1 = '<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.13.3/dist/cdn.min.js"></script>'
new_cdn2 = '<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js"></script>'

content = content.replace(old_cdn1, new_cdn1).replace(old_cdn2, new_cdn2)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
