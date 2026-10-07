import os

path = "config/middleware.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "\"script-src 'self' 'unsafe-inline' https:; \"",
    "\"script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; \""
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
