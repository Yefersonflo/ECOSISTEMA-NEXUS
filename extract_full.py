import re

with open("rendered_trd_2.html", "r", encoding="utf-8") as f:
    content = f.read()

script = re.search(r"<script>\s*function formTRDData\(\).*?</script>", content, re.DOTALL).group(0)
script = script.replace("<script>", "").replace("</script>", "")
script += "\nconst obj = formTRDData(); console.log(Object.keys(obj).length);"

with open("test_full_alpine.js", "w", encoding="utf-8") as f:
    f.write(script)
