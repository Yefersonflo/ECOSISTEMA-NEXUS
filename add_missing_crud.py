import os

views_crud_content = """
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from trd.models import EncabezadoTRD, ItemTRD
from trd.utils import catalogo_ccd

def normalizar_disposicion(disp):
    d = disp.strip().upper()
    if d in ("C", "CONSERVACION", "CONSERVACIÓN"): return "C"
    if d in ("E", "ELIMINACION", "ELIMINACIÓN"): return "E"
    if d in ("M", "MICROFILMACION", "MICROFILMACIÓN", "DIGITALIZACION", "DIGITALIZACIÓN"): return "M"
    if d in ("S", "SELECCION", "SELECCIÓN"): return "S"
    return "C"

def _entero(valor):
    try:
        return int(valor)
    except (ValueError, TypeError):
        return 0

@require_POST
def crear_nueva_version(request, enc_id):
    viejo = get_object_or_404(EncabezadoTRD, id=enc_id)
    es_copia = request.POST.get('tipo_copia') == 'copia_completa'
    
    nuevo = EncabezadoTRD.objects.create(
        entidad_productora=viejo.entidad_productora,
        oficina_productora=viejo.oficina_productora,
        fecha_creacion=timezone.now().strftime("%Y-%m-%d"),
        fecha_ajuste='',
        fecha_aprobacion='',
        fecha_convalidacion='',
        responsable_gestion_documental=viejo.responsable_gestion_documental,
        cargo_responsable_gestion_documental=viejo.cargo_responsable_gestion_documental,
        superior_jerarquico=viejo.superior_jerarquico,
        cargo_superior_jerarquico=viejo.cargo_superior_jerarquico,
        version=str(float(viejo.version) + 1.0) if viejo.version.replace('.','',1).isdigit() else f"{viejo.version}_nueva",
        estado='VIGENTE',
        vigencia_ano=str(timezone.now().year)
    )
    
    if es_copia:
        # Clone items
        items = list(viejo.items.all())
        id_map = {}
        # Parent first
        for item in sorted(items, key=lambda x: (x.parent_id is not None, x.id)):
            nuevo_parent_id = id_map.get(item.parent_id) if item.parent_id else None
            nuevo_item = ItemTRD.objects.create(
                encabezado=nuevo,
                parent_id=nuevo_parent_id,
                codigo=item.codigo,
                nivel=item.nivel,
                nombre=item.nombre,
                soporte_papel=item.soporte_papel,
                soporte_electronico=item.soporte_electronico,
                extensiones=item.extensiones,
                retencion_gestion=item.retencion_gestion,
                retencion_central=item.retencion_central,
                disposicion_final=item.disposicion_final,
                reproduccion_tecnica=item.reproduccion_tecnica,
                procedimiento=item.procedimiento,
                orden=item.orden
            )
            id_map[item.id] = nuevo_item.id
            
    # set old as HISTORICO
    viejo.estado = 'HISTORICO'
    viejo.save()
    
    messages.success(request, "Nueva versión creada exitosamente.")
    return redirect('trd:editar_trd', enc_id=nuevo.id)

@require_POST
def crear_item(request, enc_id):
    encabezado = get_object_or_404(EncabezadoTRD, id=enc_id)
    data = json.loads(request.POST.get('estructura_arbol_json', '{}'))
    if not data:
        messages.error(request, "Datos de serie inválidos.")
        return redirect('trd:editar_trd', enc_id=enc_id)
        
    serie_cod = str(data.get("serie_codigo", "")).strip()
    serie_nom = str(data.get("serie_nombre", "")).strip()
    
    if not serie_cod or not serie_nom:
        messages.error(request, "Debe especificar el código y el nombre de la Serie.")
        return redirect('trd:editar_trd', enc_id=enc_id)
        
    tiene_subserie = bool(data.get("tiene_subserie", False))
    subseries_lista = data.get("subseries", []) if tiene_subserie else []
    tipos_serie = data.get("tipos_documentales", []) if not tiene_subserie else []
    
    # Check if serie exists
    serie, created = ItemTRD.objects.get_or_create(
        encabezado=encabezado, codigo=serie_cod, nivel="Serie",
        defaults={
            "nombre": serie_nom, "parent_id": None, "soporte_papel": True, "disposicion_final": "C"
        }
    )
    if not created:
        serie.nombre = serie_nom
        serie.save()
        
    for sub_idx, sub_data in enumerate(subseries_lista):
        sub_cod = str(sub_data.get("codigo", "")).strip()
        sub_nom = str(sub_data.get("nombre", "")).strip()
        if not sub_cod or not sub_nom: continue
        
        sub_elec = bool(sub_data.get("soporte_electronico", False))
        sub_papel = bool(sub_data.get("soporte_papel", True))
        sub_ext = str(sub_data.get("extensiones", "")).strip() if sub_elec else ""
        
        sub_item, _ = ItemTRD.objects.update_or_create(
            encabezado=encabezado, codigo=sub_cod, parent_id=serie.id, nivel="Subserie",
            defaults={
                "nombre": sub_nom,
                "soporte_papel": sub_papel,
                "soporte_electronico": sub_elec,
                "extensiones": sub_ext,
                "retencion_gestion": _entero(sub_data.get("retencion_gestion")),
                "retencion_central": _entero(sub_data.get("retencion_central")),
                "disposicion_final": normalizar_disposicion(sub_data.get("disposicion_final", "C")),
                "reproduccion_tecnica": str(sub_data.get("reproduccion_tecnica", "")),
                "procedimiento": str(sub_data.get("procedimiento", "")),
                "orden": sub_idx
            }
        )
        
        for t_idx, td_data in enumerate(sub_data.get("tipos_documentales", [])):
            td_nom = str(td_data.get("nombre", "")).strip()
            if not td_nom: continue
            td_elec = bool(td_data.get("soporte_electronico", False))
            td_ext = str(td_data.get("extensiones", "")).strip() if td_elec else ""
            ItemTRD.objects.update_or_create(
                encabezado=encabezado, parent_id=sub_item.id, nombre=td_nom, nivel="Tipo",
                defaults={
                    "codigo": sub_cod,
                    "soporte_papel": bool(td_data.get("soporte_papel", True)),
                    "soporte_electronico": td_elec,
                    "extensiones": td_ext,
                    "disposicion_final": "C",
                    "orden": t_idx
                }
            )
            
    for t_idx, td_data in enumerate(tipos_serie):
        td_nom = str(td_data.get("nombre", "")).strip()
        if not td_nom: continue
        td_elec = bool(td_data.get("soporte_electronico", False))
        td_ext = str(td_data.get("extensiones", "")).strip() if td_elec else ""
        ItemTRD.objects.update_or_create(
            encabezado=encabezado, parent_id=serie.id, nombre=td_nom, nivel="Tipo",
            defaults={
                "codigo": serie_cod,
                "soporte_papel": bool(td_data.get("soporte_papel", True)),
                "soporte_electronico": td_elec,
                "extensiones": td_ext,
                "disposicion_final": "C",
                "orden": t_idx
            }
        )
        
    messages.success(request, f"Serie '{serie_nom}' guardada exitosamente.")
    return redirect('trd:editar_trd', enc_id=enc_id)

@require_POST
def agregar_subserie_directa(request, enc_id, serie_id):
    encabezado = get_object_or_404(EncabezadoTRD, id=enc_id)
    serie = get_object_or_404(ItemTRD, id=serie_id, encabezado=encabezado)
    
    sub_cod = request.POST.get("codigo", "").strip()
    sub_nom = request.POST.get("nombre", "").strip()
    if not sub_cod or not sub_nom:
        messages.error(request, "El código y nombre son obligatorios.")
        return redirect('trd:editar_trd', enc_id=enc_id)
        
    sub_elec = request.POST.get("soporte_electronico") in ("1", "true", "on")
    sub_ext = request.POST.get("extensiones", "").strip() if sub_elec else ""
    
    ItemTRD.objects.create(
        encabezado=encabezado, parent_id=serie.id, codigo=sub_cod, nombre=sub_nom, nivel="Subserie",
        soporte_papel=request.POST.get("soporte_papel") in ("1", "true", "on"),
        soporte_electronico=sub_elec,
        extensiones=sub_ext,
        retencion_gestion=_entero(request.POST.get("retencion_gestion")),
        retencion_central=_entero(request.POST.get("retencion_central")),
        disposicion_final=normalizar_disposicion(request.POST.get("disposicion_final", "")),
        reproduccion_tecnica=request.POST.get("reproduccion_tecnica", "").strip().upper(),
        procedimiento=request.POST.get("procedimiento", "").strip(),
        orden=ItemTRD.objects.filter(parent_id=serie.id, nivel="Subserie").count()
    )
    
    messages.success(request, f"Subserie '{sub_nom}' agregada exitosamente.")
    return redirect('trd:editar_trd', enc_id=enc_id)

@require_POST
def agregar_tipo_documental(request, enc_id, padre_id):
    encabezado = get_object_or_404(EncabezadoTRD, id=enc_id)
    padre = get_object_or_404(ItemTRD, id=padre_id, encabezado=encabezado)
    
    td_nom = request.POST.get("nombre", "").strip()
    if not td_nom:
        messages.error(request, "El nombre del tipo documental es obligatorio.")
        return redirect('trd:editar_trd', enc_id=enc_id)
        
    td_elec = request.POST.get("soporte_electronico") in ("1", "true", "on")
    td_ext = request.POST.get("extensiones", "").strip() if td_elec else ""
    
    ItemTRD.objects.create(
        encabezado=encabezado, parent_id=padre.id, codigo=padre.codigo, nombre=td_nom, nivel="Tipo",
        soporte_papel=request.POST.get("soporte_papel") in ("1", "true", "on"),
        soporte_electronico=td_elec,
        extensiones=td_ext,
        disposicion_final="C",
        orden=ItemTRD.objects.filter(parent_id=padre.id, nivel="Tipo").count()
    )
    
    messages.success(request, f"Tipo documental '{td_nom}' agregado.")
    return redirect('trd:editar_trd', enc_id=enc_id)

@require_POST
def editar_campo_inline(request, enc_id, item_id):
    item = get_object_or_404(ItemTRD, id=item_id, encabezado_id=enc_id)
    campo = request.POST.get("campo")
    valor = request.POST.get("valor", "").strip()
    
    if campo in ("retencion_gestion", "retencion_central", "orden"):
        setattr(item, campo, _entero(valor))
    elif campo in ("soporte_papel", "soporte_electronico"):
        setattr(item, campo, valor.lower() in ("true", "1", "yes"))
    elif campo == "disposicion_final":
        setattr(item, campo, normalizar_disposicion(valor))
    elif campo in ("nombre", "codigo", "reproduccion_tecnica", "procedimiento", "extensiones"):
        setattr(item, campo, valor)
        
    item.save()
    messages.success(request, f"Campo {campo} actualizado.")
    return redirect('trd:editar_trd', enc_id=enc_id)

@require_POST
def eliminar_item(request, enc_id, item_id):
    item = get_object_or_404(ItemTRD, id=item_id, encabezado_id=enc_id)
    
    def cascade_delete(parent_id):
        children = ItemTRD.objects.filter(parent_id=parent_id)
        for child in children:
            cascade_delete(child.id)
            child.delete()
            
    cascade_delete(item.id)
    item.delete()
    
    messages.success(request, "Elemento eliminado correctamente.")
    return redirect('trd:editar_trd', enc_id=enc_id)
"""

with open("trd/views_crud.py", "w", encoding="utf-8") as f:
    f.write(views_crud_content)

urls_path = "trd/urls.py"
with open(urls_path, "r", encoding="utf-8") as f:
    urls_content = f.read()

new_urls = """
    path('<int:enc_id>/nueva_version', views_crud.crear_nueva_version, name='crear_nueva_version'),
    path('<int:enc_id>/item', views_crud.crear_item, name='crear_item'),
    path('<int:enc_id>/serie/<int:serie_id>/agregar_subserie', views_crud.agregar_subserie_directa, name='agregar_subserie_directa'),
    path('<int:enc_id>/item/<int:padre_id>/agregar_tipo', views_crud.agregar_tipo_documental, name='agregar_tipo_documental'),
    path('<int:enc_id>/item/<int:item_id>/editar', views_crud.editar_campo_inline, name='editar_campo_inline'),
    path('<int:enc_id>/item/<int:item_id>/eliminar', views_crud.eliminar_item, name='eliminar_item'),
"""

if "crear_item" not in urls_content:
    urls_content = urls_content.replace("from . import views", "from . import views, views_crud")
    # Insert new urls before api endpoints
    urls_content = urls_content.replace("    # API endpoints", new_urls + "\n    # API endpoints")
    with open(urls_path, "w", encoding="utf-8") as f:
        f.write(urls_content)
