import os

path = "trd/views.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_logic = """
    for oficina, items_oficina in items_por_oficina.items():
        oficinas_tarjetas.append({
            "nombre": oficina,
            "series": agrupar_items_jerarquia(items_oficina),
            "total_items": len(items_oficina)
        })
    oficinas_tarjetas.sort(key=lambda x: x["nombre"])
"""

new_logic = """
    for oficina, items_oficina in items_por_oficina.items():
        total_series = sum(1 for i in items_oficina if i.nivel == NIVEL_SERIE)
        total_subseries = sum(1 for i in items_oficina if i.nivel == NIVEL_SUBSERIE)
        total_tipos = sum(1 for i in items_oficina if i.nivel == NIVEL_TIPO)
        
        enc_id = None
        if items_oficina and items_oficina[0].encabezado:
            enc_id = items_oficina[0].encabezado.id

        oficinas_tarjetas.append({
            "oficina_productora": oficina,
            "encabezado_id": enc_id,
            "total_series": total_series,
            "total_subseries": total_subseries,
            "total_tipos": total_tipos,
            "series": agrupar_items_jerarquia(items_oficina)
        })
    oficinas_tarjetas.sort(key=lambda x: x["oficina_productora"])
"""

content = content.replace(old_logic, new_logic)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
