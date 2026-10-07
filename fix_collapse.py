import re

with open("templates/layout/base.html", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("x-collapse", 'x-transition:enter="transition ease-out duration-200" x-transition:enter-start="opacity-0 -translate-y-2" x-transition:enter-end="opacity-100 translate-y-0" x-transition:leave="transition ease-in duration-150" x-transition:leave-start="opacity-100 translate-y-0" x-transition:leave-end="opacity-0 -translate-y-2"')

with open("templates/layout/base.html", "w", encoding="utf-8") as f:
    f.write(content)
