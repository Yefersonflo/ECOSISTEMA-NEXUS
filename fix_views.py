import os

with open("trd/views.py", "r", encoding="utf-8") as f:
    content = f.read()

import re
new_inicio = """def inicio(request):
    # Limpiar automáticamente tablas huérfanas/borradores vacíos sin series
    EncabezadoTRD.objects.filter(items__isnull=True).delete()
    
    stats = {
        'oficinas': OficinaProductora.objects.count() if OficinaProductora.objects.exists() else 0,
        'tablas': EncabezadoTRD.objects.count(),
        'items': ItemTRD.objects.count(),
        'conservacion': ItemTRD.objects.filter(disposicion_final__in=['C', 'Conservación', 'Conservacion']).count()
    }
    tablas = EncabezadoTRD.objects.all().order_by('-id')
    return render(request, "trd/inicio.html", {"stats": stats, "tablas": tablas})"""

content = re.sub(r"def inicio\(request\):.*?return render\(.*?inicio\.html.*?tablas\}\)", new_inicio, content, flags=re.DOTALL)
# Make sure render path is 'trd/inicio.html' and others as well
content = content.replace('"inicio.html"', '"trd/inicio.html"')
content = content.replace('"diligenciar.html"', '"trd/diligenciar.html"')
content = content.replace('"editar_trd.html"', '"trd/editar_trd.html"')
content = content.replace('"catalogo.html"', '"trd/catalogo.html"')
content = content.replace('"oficinas.html"', '"trd/oficinas.html"')

with open("trd/views.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated views.py template paths and stats")
