import os, django
import sqlite3

# This script will run on the VPS container
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from trd.models import EncabezadoTRD, ItemTRD

# Connect to sqlite
conn = sqlite3.connect('/app/trd_database.db')
cursor = conn.cursor()

cursor.execute("SELECT id, entidad_productora, oficina_productora, fecha_creacion, fecha_ajuste, fecha_aprobacion, fecha_convalidacion, responsable_gestion_documental, superior_jerarquico, cargo_responsable, cargo_superior, version, estado, vigencia_ano, responsable_area, cargo_responsable_area FROM trd_encabezados")
encabezados = cursor.fetchall()

# Map old ID to new ID
id_map_enc = {}
id_map_item = {}

for enc in encabezados:
    old_id = enc[0]
    # Check if already exists?
    # Delete old first to be safe
    # EncabezadoTRD.objects.all().delete() # No, let's not delete, just insert if not exists
    new_enc = EncabezadoTRD.objects.create(
        entidad_productora=enc[1] or "",
        oficina_productora=enc[2] or "",
        fecha_creacion=enc[3] or "",
        fecha_ajuste=enc[4] or "",
        fecha_aprobacion=enc[5] or "",
        fecha_convalidacion=enc[6] or "",
        responsable_gestion_documental=enc[7] or "",
        superior_jerarquico=enc[8] or "",
        cargo_responsable_gestion_documental=enc[9] or "",
        cargo_superior_jerarquico=enc[10] or "",
        version=enc[11] or "1.0",
        estado=enc[12] or "VIGENTE",
        vigencia_ano=enc[13] or "",
        responsable_area=enc[14] or "",
        cargo_responsable_area=enc[15] or "",
    )
    id_map_enc[old_id] = new_enc

cursor.execute("SELECT id, encabezado_id, parent_id, codigo, nivel, nombre, soporte_papel, soporte_electronico, extensiones, retencion_gestion, retencion_central, disposicion_final, reproduccion_tecnica, procedimiento, orden FROM trd_items ORDER BY parent_id NULLS FIRST")
items = cursor.fetchall()

# Parents first is somewhat handled by NULLS FIRST, but let's be careful.
# Wait, parent_id must exist before creating the child.
# Let's insert in passes.

pending = items.copy()
inserted_count = 0

while pending:
    for item in pending.copy():
        old_id = item[0]
        enc_id = item[1]
        parent_id = item[2]
        
        if enc_id not in id_map_enc:
            pending.remove(item)
            continue
            
        new_parent = None
        if parent_id:
            if parent_id not in id_map_item:
                continue # Wait for parent
            new_parent = id_map_item[parent_id]
            
        new_item = ItemTRD.objects.create(
            encabezado=id_map_enc[enc_id],
            parent=new_parent,
            codigo=item[3] or "",
            nivel=item[4],
            nombre=item[5] or "",
            soporte_papel=bool(item[6]),
            soporte_electronico=bool(item[7]),
            extensiones=item[8] or "",
            retencion_gestion=item[9] or 0,
            retencion_central=item[10] or 0,
            disposicion_final=item[11] or "",
            reproduccion_tecnica=bool(item[12]),
            procedimiento=item[13] or "",
            orden=item[14] or 0
        )
        id_map_item[old_id] = new_item
        pending.remove(item)
        inserted_count += 1

print(f"Migrados {len(id_map_enc)} encabezados y {inserted_count} items!")
