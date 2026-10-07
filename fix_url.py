with open('trd/templates/trd/diligenciar.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("{{ url_for('inicio') }}", "/")

with open('trd/templates/trd/diligenciar.html', 'w', encoding='utf-8') as f:
    f.write(content)
