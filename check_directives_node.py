import re, json

with open("rendered_trd_2.html", "r", encoding="utf-8") as f:
    content = f.read()

directives = re.findall(r'(x-show|x-text|x-model|@click|:class|:value|x-if)="([^"]+)"', content)
directives += re.findall(r"(x-show|x-text|x-model|@click|:class|:value|x-if)='([^']+)'", content)

js_code = ""
for attr, val in directives:
    # Wrap in function to check syntax
    if "{" in val and attr != ":class":
        pass # might be object
    
    js_code += f"try {{ new Function({json.dumps(val)}); }} catch(e) {{ console.log('Error in {attr}:', e.message, 'Code:', {json.dumps(val)}); }}\n"

with open("check_alpine_syntax.js", "w", encoding="utf-8") as f:
    f.write(js_code)

