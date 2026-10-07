import os

tpl_dir = "trd/templates/trd"
for file in os.listdir(tpl_dir):
    if file.endswith(".html"):
        path = os.path.join(tpl_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.replace("loop.index", "forloop.counter")
        content = content.replace("loop.index0", "forloop.counter0")
        content = content.replace("request.args", "request.GET")

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
print("Loop vars converted.")
