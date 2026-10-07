import os
import re

tpl_dir = "trd/templates/trd"
for file in os.listdir(tpl_dir):
    if file.endswith(".html"):
        path = os.path.join(tpl_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace url_for('route') -> {% url 'trd:route' %}
        # Handle cases with kwargs like url_for('editar_trd', enc_id=t.id) -> {% url 'trd:editar_trd' enc_id=t.id %}
        def repl(match):
            inner = match.group(1)
            parts = inner.split(',')
            route = parts[0].strip().strip("'\"")
            args = " ".join([p.strip().replace("=", "=") for p in parts[1:]])
            args = args.replace("=", "=") # Actually in Django url tag it is arg=val or just arg
            if args:
                return f"{{% url 'trd:{route}' {args} %}}"
            else:
                return f"{{% url 'trd:{route}' %}}"
                
        content = re.sub(r"\{\{\s*url_for\((.*?)\)\s*\}\}", repl, content)
        
        # In Django, length filter is |length, in Jinja it's |length but sometimes 	.items|length works differently? It's fine.
        # Jinja set -> Django with (but usually we can't replace it simply)
        # Let's remove {% set %} and try to use inline
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

print("Templates converted.")
