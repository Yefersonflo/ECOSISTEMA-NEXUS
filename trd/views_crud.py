from django.db.models import Max

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
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

@login_required
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
        titulo_responsable_1=getattr(viejo, 'titulo_responsable_1', None) or 'Responsable del área de gestión documental de la entidad',
        responsable_gestion_documental=viejo.responsable_gestion_documental,
        cargo_responsable_gestion_documental=viejo.cargo_responsable_gestion_documental,
        titulo_responsable_2=getattr(viejo, 'titulo_responsable_2', None) or 'Responsable de Área',
        responsable_area=viejo.responsable_area,
        cargo_responsable_area=viejo.cargo_responsable_area,
        titulo_responsable_3=getattr(viejo, 'titulo_responsable_3', None) or 'Subdirectora Administrativa y financiera',
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

@login_required
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
    
    from trd.utils import oficinas
    pref = oficinas.prefijo_de(encabezado.oficina_productora)
    if pref and serie_cod and not serie_cod.startswith(pref + "."):
        serie_cod = f"{pref}.{serie_cod}"
    serie_nom = serie_nom.upper()

    serie_papel = bool(data.get("serie_soporte_papel", False))
    serie_elec = bool(data.get("serie_soporte_electronico", False))
    serie_ext = str(data.get("serie_extensiones", "")).strip() if serie_elec else ""
    serie_ret_g = _entero(data.get("serie_retencion_gestion", 0))
    serie_ret_c = _entero(data.get("serie_retencion_central", 0))
    serie_disp_raw = str(data.get("serie_disposicion_final", "")).strip()
    serie_disp = normalizar_disposicion(serie_disp_raw) if serie_disp_raw else ""
    serie_rep = str(data.get("serie_reproduccion_tecnica", "")).strip().upper()
    serie_proc = str(data.get("procedimiento", "")).strip()

    serie = ItemTRD.objects.filter(encabezado=encabezado, codigo=serie_cod, parent_id__isnull=True).first()
    if serie:
        serie.nivel = "SERIE"
        serie.nombre = serie_nom
        serie.soporte_papel = serie_papel
        serie.soporte_electronico = serie_elec
        serie.extensiones = serie_ext
        serie.retencion_gestion = serie_ret_g
        serie.retencion_central = serie_ret_c
        serie.disposicion_final = serie_disp
        serie.reproduccion_tecnica = serie_rep
        serie.procedimiento = serie_proc
        serie.save()
    else:
        serie = ItemTRD.objects.create(
            encabezado=encabezado,
            parent_id=None,
            codigo=serie_cod,
            nivel="SERIE",
            nombre=serie_nom,
            soporte_papel=serie_papel,
            soporte_electronico=serie_elec,
            extensiones=serie_ext,
            retencion_gestion=serie_ret_g,
            retencion_central=serie_ret_c,
            disposicion_final=serie_disp,
            reproduccion_tecnica=serie_rep,
            procedimiento=serie_proc,
        )

    for sub_idx, sub_data in enumerate(subseries_lista):
        sub_cod = str(sub_data.get("codigo", "")).strip()
        sub_nom = str(sub_data.get("nombre", "")).strip()
        if not sub_cod or not sub_nom: continue
        if pref and not sub_cod.startswith(pref + "."):
            sub_cod = f"{pref}.{sub_cod}"

        sub_elec = bool(sub_data.get("soporte_electronico", False))
        sub_papel = bool(sub_data.get("soporte_papel", False))
        sub_ext = str(sub_data.get("extensiones", "")).strip() if sub_elec else ""
        sub_disp_raw = str(sub_data.get("disposicion_final", "")).strip()
        sub_disp = normalizar_disposicion(sub_disp_raw) if sub_disp_raw else ""

        sub_item = ItemTRD.objects.filter(encabezado=encabezado, codigo=sub_cod, parent_id=serie.id).first()
        if sub_item:
            sub_item.nivel = "SUBSERIE"
            sub_item.nombre = sub_nom
            sub_item.soporte_papel = sub_papel
            sub_item.soporte_electronico = sub_elec
            sub_item.extensiones = sub_ext
            sub_item.retencion_gestion = _entero(sub_data.get("retencion_gestion"))
            sub_item.retencion_central = _entero(sub_data.get("retencion_central"))
            sub_item.disposicion_final = sub_disp
            sub_item.reproduccion_tecnica = str(sub_data.get("reproduccion_tecnica", "")).strip().upper()
            sub_item.procedimiento = str(sub_data.get("procedimiento", "")).strip()
            sub_item.orden = sub_idx
            sub_item.save()
        else:
            sub_item = ItemTRD.objects.create(
                encabezado=encabezado, codigo=sub_cod, parent_id=serie.id, nivel="SUBSERIE",
                nombre=sub_nom,
                soporte_papel=sub_papel,
                soporte_electronico=sub_elec,
                extensiones=sub_ext,
                retencion_gestion=_entero(sub_data.get("retencion_gestion")),
                retencion_central=_entero(sub_data.get("retencion_central")),
                disposicion_final=sub_disp,
                reproduccion_tecnica=str(sub_data.get("reproduccion_tecnica", "")).strip().upper(),
                procedimiento=str(sub_data.get("procedimiento", "")).strip(),
                orden=sub_idx
            )

        max_ord_sub = ItemTRD.objects.filter(parent_id=sub_item.id, nivel="TIPO DOCUMENTAL").aggregate(Max('orden'))['orden__max'] or 0
        for td_data in sub_data.get("tipos_documentales", []):
            td_nom = str(td_data.get("nombre", "")).strip()
            if not td_nom: continue
            td_elec = bool(td_data.get("soporte_electronico", False))
            td_papel = bool(td_data.get("soporte_papel", False))
            if not td_papel and not td_elec:
                td_papel = True
            td_ext = str(td_data.get("extensiones", "")).strip() if td_elec else ""
            existente_td = ItemTRD.objects.filter(encabezado=encabezado, parent_id=sub_item.id, nombre=td_nom, nivel="TIPO DOCUMENTAL").first()
            if existente_td:
                existente_td.soporte_papel = td_papel
                existente_td.soporte_electronico = td_elec
                existente_td.extensiones = td_ext
                existente_td.save()
            else:
                max_ord_sub += 1
                ItemTRD.objects.create(
                    encabezado=encabezado, parent_id=sub_item.id, nombre=td_nom, nivel="TIPO DOCUMENTAL",
                    codigo=f"{sub_cod}.{max_ord_sub}",
                    soporte_papel=td_papel,
                    soporte_electronico=td_elec,
                    extensiones=td_ext,
                    disposicion_final="C",
                    orden=max_ord_sub
                )
            
    max_ord_serie = ItemTRD.objects.filter(parent_id=serie.id, nivel="TIPO DOCUMENTAL").aggregate(Max('orden'))['orden__max'] or 0
    for td_data in tipos_serie:
        td_nom = str(td_data.get("nombre", "")).strip()
        if not td_nom: continue
        td_elec = bool(td_data.get("soporte_electronico", False))
        td_papel = bool(td_data.get("soporte_papel", False))
        if not td_papel and not td_elec:
            td_papel = True
        td_ext = str(td_data.get("extensiones", "")).strip() if td_elec else ""
        existente_td = ItemTRD.objects.filter(encabezado=encabezado, parent_id=serie.id, nombre=td_nom, nivel="TIPO DOCUMENTAL").first()
        if existente_td:
            existente_td.soporte_papel = td_papel
            existente_td.soporte_electronico = td_elec
            existente_td.extensiones = td_ext
            existente_td.save()
        else:
            max_ord_serie += 1
            ItemTRD.objects.create(
                encabezado=encabezado, parent_id=serie.id, nombre=td_nom, nivel="TIPO DOCUMENTAL",
                codigo=f"{serie_cod}.{max_ord_serie}",
                soporte_papel=td_papel,
                soporte_electronico=td_elec,
                extensiones=td_ext,
                disposicion_final="C",
                orden=max_ord_serie
            )
        
    try:
        if tiene_subserie:
            for sub_data in subseries_lista:
                catalogo_ccd.registrar_serie_o_subserie_personalizada(
                    nombre_o_prefijo=encabezado.oficina_productora,
                    serie_cod=serie_cod,
                    serie_nom=serie_nom,
                    sub_cod=str(sub_data.get("codigo", "")).strip(),
                    sub_nom=str(sub_data.get("nombre", "")).strip(),
                )
        else:
            catalogo_ccd.registrar_serie_o_subserie_personalizada(
                nombre_o_prefijo=encabezado.oficina_productora,
                serie_cod=serie_cod,
                serie_nom=serie_nom,
            )
    except Exception:
        pass

    messages.success(request, f"Serie '{serie_nom}' guardada exitosamente.")
    return redirect('trd:editar_trd', enc_id=enc_id)

@login_required
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
        encabezado=encabezado, parent_id=serie.id, codigo=sub_cod, nombre=sub_nom, nivel="SUBSERIE",
        soporte_papel=request.POST.get("soporte_papel") in ("1", "true", "on"),
        soporte_electronico=sub_elec,
        extensiones=sub_ext,
        retencion_gestion=_entero(request.POST.get("retencion_gestion")),
        retencion_central=_entero(request.POST.get("retencion_central")),
        disposicion_final=normalizar_disposicion(request.POST.get("disposicion_final", "")),
        reproduccion_tecnica=request.POST.get("reproduccion_tecnica", "").strip().upper(),
        procedimiento=request.POST.get("procedimiento", "").strip(),
        orden=(ItemTRD.objects.filter(parent_id=serie.id, nivel="SUBSERIE").aggregate(Max("orden"))["orden__max"] or 0) + 1
    )
    
    messages.success(request, f"Subserie '{sub_nom}' agregada exitosamente.")
    return redirect('trd:editar_trd', enc_id=enc_id)

@login_required
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
    
    sig_orden = (ItemTRD.objects.filter(parent_id=padre.id, nivel="TIPO DOCUMENTAL").aggregate(Max("orden"))["orden__max"] or 0) + 1
    td_papel = request.POST.get("soporte_papel") in ("1", "true", "on")
    if not td_papel and not td_elec:
        td_papel = True
    ItemTRD.objects.create(
        encabezado=encabezado, parent_id=padre.id, codigo=f"{padre.codigo}.{sig_orden}", nombre=td_nom, nivel="TIPO DOCUMENTAL",
        soporte_papel=td_papel,
        soporte_electronico=td_elec,
        extensiones=td_ext,
        disposicion_final="C",
        orden=sig_orden
    )
    
    messages.success(request, f"Tipo documental '{td_nom}' agregado.")
    return redirect('trd:editar_trd', enc_id=enc_id)

@login_required
@require_POST
def editar_campo_inline(request, enc_id, item_id):
    item = get_object_or_404(ItemTRD, id=item_id, encabezado_id=enc_id)
    campo = request.POST.get("campo")
    
    if campo:
        valor = request.POST.get("valor", "").strip()
        if campo in ("retencion_gestion", "retencion_central", "orden"):
            setattr(item, campo, _entero(valor))
        elif campo in ("soporte_papel", "soporte_electronico"):
            setattr(item, campo, valor.lower() in ("true", "1", "yes"))
        elif campo == "disposicion_final":
            setattr(item, campo, normalizar_disposicion(valor))
        elif campo in ("nombre", "codigo", "reproduccion_tecnica", "procedimiento", "extensiones"):
            setattr(item, campo, valor)
        messages.success(request, f"Campo {campo} actualizado.")
    else:
        # Actualización completa desde modal de edición
        is_tipo_doc = item.nivel.strip().upper() == "TIPO DOCUMENTAL"
        if "nombre" in request.POST:
            item.nombre = request.POST.get("nombre", "").strip()
        if not is_tipo_doc and "codigo" in request.POST:
            item.codigo = request.POST.get("codigo", "").strip()
            
        item.soporte_papel = request.POST.get("soporte_papel") in ("1", "true", "on")
        item.soporte_electronico = request.POST.get("soporte_electronico") in ("1", "true", "on")
        item.extensiones = request.POST.get("extensiones", "").strip() if item.soporte_electronico else ""
        
        if not is_tipo_doc:
            if "retencion_gestion" in request.POST:
                item.retencion_gestion = _entero(request.POST.get("retencion_gestion"))
            if "retencion_central" in request.POST:
                item.retencion_central = _entero(request.POST.get("retencion_central"))
            if "disposicion_final" in request.POST:
                item.disposicion_final = normalizar_disposicion(request.POST.get("disposicion_final", ""))
            item.reproduccion_tecnica = request.POST.get("reproduccion_tecnica", "").strip().upper()
            item.procedimiento = request.POST.get("procedimiento", "").strip()
            
        messages.success(request, f"{item.nivel} '{item.nombre}' actualizado exitosamente.")
        
    item.save()
    return redirect('trd:editar_trd', enc_id=enc_id)

@login_required
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
