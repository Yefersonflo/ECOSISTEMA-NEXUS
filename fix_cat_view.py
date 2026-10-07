import os

path = "trd/views.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

group_logic = """
    oficinas_tarjetas = []
    items_por_oficina = {}
    for item in qs:
        oficina = item.encabezado.oficina_productora if item.encabezado else "SIN OFICINA"
        if oficina not in items_por_oficina:
            items_por_oficina[oficina] = []
        items_por_oficina[oficina].append(item)
    
    for oficina, items_oficina in items_por_oficina.items():
        oficinas_tarjetas.append({
            "nombre": oficina,
            "series": agrupar_items_jerarquia(items_oficina),
            "total_items": len(items_oficina)
        })
    oficinas_tarjetas.sort(key=lambda x: x["nombre"])

    return render(request, "trd/catalogo.html", {
        "resultados": list(qs),
        "oficinas_tarjetas": oficinas_tarjetas,
"""

content = content.replace(
    'return render(request, "trd/catalogo.html", {\n        "resultados": resultados,',
    group_logic
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
