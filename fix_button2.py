import os

path = "templates/layout/base.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("https://trd.nexusflz.tech/", "{% url 'trd:inicio' %}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
