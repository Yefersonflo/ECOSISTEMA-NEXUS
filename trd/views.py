import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

def is_trd_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.rol in ['SUPER', 'JEFE'])

from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Count, Q

from .models import EncabezadoTRD, ItemTRD, OficinaProductora

try:
    from .utils.pdf_exporter import generar_pdf, generar_pdf_consolidado
    from .utils.exporter import generar_xlsx
except ImportError:
    pass

try:
    from .utils import catalogo_ccd
except ImportError:
    pass

# Constants
CODIGO_FORMATO = "PADO308-PR004-FADO004"
VERSION_FORMATO = "1.0"
DISPOSICIONES = {"C": "Conservación", "E": "Eliminación", "M": "Microfilmación", "S": "Selección"}
REPRODUCCIONES = {"M": "Microfilmación", "D": "Digitalización"}
NIVELES = ["SERIE", "SUBSERIE", "TIPO"]
ENTIDAD_POR_DEFECTO = "COMFACASANARE"
NIVEL_SERIE = "SERIE"
NIVEL_SUBSERIE = "SUBSERIE"
NIVEL_TIPO = "TIPO DOCUMENTAL"

def normalizar_disposicion(disp):
    disp = str(disp).strip().upper()
    return disp if disp in DISPOSICIONES else ""

def _entero(valor):
    try:
        return int(str(valor).strip())
    except (TypeError, ValueError):
        return 0

def agrupar_items_jerarquia(items):
    series = []
    serie_actual = None
    subserie_actual = None
    series_map = {}
    subseries_map = {}

    for i in items:
        if i.nivel == NIVEL_SERIE:
            serie_nodo = {
                "serie": i,
                "subseries": [],
                "tipos_directos": [],
                "total_hijos": 0,
            }
            series.append(serie_nodo)
            if i.id:
                series_map[i.id] = serie_nodo
            serie_actual = serie_nodo
            subserie_actual = None
        elif i.nivel == NIVEL_SUBSERIE:
            sub_nodo = {
                "subserie": i,
                "tipos": [],
            }
            target_serie = series_map.get(i.parent_id) if i.parent_id else serie_actual
            if target_serie:
                target_serie["subseries"].append(sub_nodo)
                target_serie["total_hijos"] += 1
            else:
                serie_virtual = {
                    "serie": ItemTRD(
                        codigo=i.codigo.rsplit(".", 1)[0] if "." in i.codigo else i.codigo,
                        nivel=NIVEL_SERIE,
                        nombre="SERIE",
                        id=None,
                    ),
                    "subseries": [sub_nodo],
                    "tipos_directos": [],
                    "total_hijos": 1,
                }
                series.append(serie_virtual)
                target_serie = serie_virtual
            if i.id:
                subseries_map[i.id] = sub_nodo
            subserie_actual = sub_nodo
        elif i.nivel == NIVEL_TIPO:
            target_sub = subseries_map.get(i.parent_id) if i.parent_id else subserie_actual
            if target_sub:
                target_sub["tipos"].append(i)
                if serie_actual:
                    serie_actual["total_hijos"] += 1
            else:
                target_serie = series_map.get(i.parent_id) if i.parent_id else serie_actual
                if target_serie:
                    target_serie["tipos_directos"].append(i)
                    target_serie["total_hijos"] += 1
                elif series:
                    series[-1]["tipos_directos"].append(i)
                    series[-1]["total_hijos"] += 1

    return series

def inicio(request):
    # Limpiar automáticamente tablas huérfanas/borradores vacíos sin series
    EncabezadoTRD.objects.filter(items__isnull=True).delete()
    
    stats = {
        'oficinas': OficinaProductora.objects.count() if OficinaProductora.objects.exists() else 0,
        'tablas': EncabezadoTRD.objects.count(),
        'items': ItemTRD.objects.count(),
        'conservacion': ItemTRD.objects.filter(disposicion_final__in=['C', 'Conservación', 'Conservacion']).count()
    }
    tablas = EncabezadoTRD.objects.all().order_by('-id')
    return render(request, "trd/inicio.html", {"stats": stats, "tablas": tablas})

def diligenciar(request):
    if request.method == "POST":
        oficina = request.POST.get("oficina_productora", "").strip()
        if not oficina:
            messages.error(request, "Debe especificar la oficina productora.")
            return redirect("trd:diligenciar")

        existente = EncabezadoTRD.objects.filter(oficina_productora=oficina).first()
        if existente:
            existente.entidad_productora = request.POST.get("entidad_productora", ENTIDAD_POR_DEFECTO).strip()
            existente.fecha_creacion = request.POST.get("fecha_creacion", "").strip()
            existente.fecha_ajuste = request.POST.get("fecha_ajuste", "").strip()
            existente.fecha_aprobacion = request.POST.get("fecha_aprobacion", "").strip()
            existente.fecha_convalidacion = request.POST.get("fecha_convalidacion", "").strip()
            existente.responsable_gestion_documental = request.POST.get("responsable", "").strip()
            existente.cargo_responsable_gestion_documental = request.POST.get("cargo_responsable", "").strip()
            existente.responsable_area = request.POST.get("responsable_area", "").strip()
            existente.cargo_responsable_area = request.POST.get("cargo_responsable_area", "").strip()
            existente.superior_jerarquico = request.POST.get("superior", "").strip()
            existente.cargo_superior_jerarquico = request.POST.get("cargo_superior", "").strip()
            existente.save()
            messages.info(request, f"Se abrió la Tabla de Retención existente de {oficina}.")
            return redirect("trd:editar_trd", enc_id=existente.id)
            
        nuevo = EncabezadoTRD.objects.create(
            oficina_productora=oficina,
            entidad_productora=request.POST.get("entidad_productora", ENTIDAD_POR_DEFECTO).strip(),
            fecha_creacion=request.POST.get("fecha_creacion", "").strip(),
            fecha_ajuste=request.POST.get("fecha_ajuste", "").strip(),
            fecha_aprobacion=request.POST.get("fecha_aprobacion", "").strip(),
            fecha_convalidacion=request.POST.get("fecha_convalidacion", "").strip(),
            responsable_gestion_documental=request.POST.get("responsable", "").strip(),
            cargo_responsable_gestion_documental=request.POST.get("cargo_responsable", "").strip(),
            responsable_area=request.POST.get("responsable_area", "").strip(),
            cargo_responsable_area=request.POST.get("cargo_responsable_area", "").strip(),
            superior_jerarquico=request.POST.get("superior", "").strip(),
            cargo_superior_jerarquico=request.POST.get("cargo_superior", "").strip()
        )
        messages.success(request, "Encabezado guardado. Ahora agregue las Series y Subseries para completar la TRD.")
        return redirect("trd:editar_trd", enc_id=nuevo.id)

    EncabezadoTRD.objects.filter(items__isnull=True).delete()
    oficinas = OficinaProductora.objects.all().order_by('nombre')
    return render(request, "trd/diligenciar.html", {
        "oficinas": oficinas,
        "entidad": ENTIDAD_POR_DEFECTO,
    })

def editar_trd(request, enc_id):
    encabezado = get_object_or_404(EncabezadoTRD, id=enc_id)
    items = list(encabezado.items.all().order_by('orden', 'codigo'))
    
    try:
        datos_ccd = catalogo_ccd.obtener_datos_oficina(encabezado.oficina_productora)
    except NameError:
        datos_ccd = {"series": []}
        
    versiones = EncabezadoTRD.objects.filter(oficina_productora=encabezado.oficina_productora).order_by('-id')

    return render(request, "trd/editar_trd.html", {
        "encabezado": encabezado,
        "enc_id": enc_id,
        "items": items,
        "arbol_series": agrupar_items_jerarquia(items),
        "padres": [i for i in items if i.nivel != NIVEL_TIPO],
        "catalogo_oficina": datos_ccd,
        "catalogo_json": json.dumps(datos_ccd or {"series": []}),
        "versiones_oficina": list(versiones),
    })

def catalogo(request):
    oficinas_sel = request.GET.getlist("oficinas")
    if not oficinas_sel and request.GET.get("oficina"):
        oficinas_sel = [request.GET.get("oficina")]

    q = request.GET.get("q", "")
    disp = request.GET.get("disposicion", "")
    nivel = request.GET.get("nivel", "")

    qs = ItemTRD.objects.select_related('encabezado')
    if oficinas_sel:
        qs = qs.filter(encabezado__oficina_productora__in=oficinas_sel)
    if q:
        qs = qs.filter(Q(nombre__icontains=q) | Q(codigo__icontains=q))
    if disp:
        qs = qs.filter(disposicion_final=disp)
    if nivel:
        qs = qs.filter(nivel=nivel)

    resultados = list(qs)
    
    conteos = {
        "total_series": qs.filter(nivel=NIVEL_SERIE).count(),
        "total_subseries": qs.filter(nivel=NIVEL_SUBSERIE).count(),
        "total_tipos": qs.filter(nivel=NIVEL_TIPO).count(),
        "total_oficinas": qs.values('encabezado__oficina_productora').distinct().count(),
        "total_general": qs.count(),
    }
    
    oficinas_all = OficinaProductora.objects.all().order_by('nombre')
    
    oficinas_tarjetas = []
    items_por_oficina = {}
    for item in qs:
        oficina = item.encabezado.oficina_productora if item.encabezado else "SIN OFICINA"
        if oficina not in items_por_oficina:
            items_por_oficina[oficina] = []
        items_por_oficina[oficina].append(item)
    
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

    return render(request, "trd/catalogo.html", {
        "resultados": list(qs),
        "oficinas_tarjetas": oficinas_tarjetas,

        "conteos": conteos,
        "oficinas": oficinas_all,
        "disposiciones": DISPOSICIONES,
        "oficinas_seleccionadas": json.dumps(oficinas_sel),
        "filtros": {
            "texto": q, "oficinas": oficinas_sel, "disposicion": disp, "nivel": nivel
        }
    })

def oficinas(request):
    ofs = OficinaProductora.objects.all().order_by('nombre')
    return render(request, "trd/oficinas.html", {"oficinas": ofs})

@require_POST
def crear_oficina(request):
    if not is_trd_admin(request.user):
        messages.error(request, 'Solo el Administrador y el Jefe de Archivo pueden crear oficinas.')
        return redirect('trd:oficinas')

    prefijo = request.POST.get("prefijo", "").strip()
    nombre = request.POST.get("nombre", "").strip()
    if not prefijo.isdigit() or not nombre:
        messages.error(request, "Indique un prefijo numérico y un nombre de oficina.")
        return redirect("trd:oficinas")
        
    if OficinaProductora.objects.filter(nombre=nombre).exists():
        messages.error(request, "Esa oficina productora ya existe.")
    else:
        OficinaProductora.objects.create(prefijo=prefijo, nombre=nombre)
        messages.success(request, f"Oficina {nombre.upper()} registrada.")
    return redirect("trd:oficinas")

@require_POST
def eliminar_oficina(request, oficina_id):
    if not is_trd_admin(request.user):
        messages.error(request, 'No tienes permisos para eliminar oficinas.')
        return redirect('trd:oficinas')

    oficina = get_object_or_404(OficinaProductora, id=oficina_id)
    oficina.delete()
    messages.success(request, "Oficina eliminada del catálogo.")
    return redirect("trd:oficinas")

def exportar(request, enc_id):
    encabezado = get_object_or_404(EncabezadoTRD, id=enc_id)
    items = list(encabezado.items.all().order_by('orden', 'codigo'))
    
    try:
        flujo = generar_xlsx(encabezado, items)
        response = HttpResponse(flujo.getvalue(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f'attachment; filename="TRD_{encabezado.oficina_productora}.xlsx"'
        return response
    except NameError:
        return HttpResponse("Exporter not found", status=500)

def exportar_pdf(request, enc_id):
    encabezado = get_object_or_404(EncabezadoTRD, id=enc_id)
    items = list(encabezado.items.all().order_by('orden', 'codigo'))
    
    try:
        flujo = generar_pdf(encabezado, items)
        response = HttpResponse(flujo.getvalue(), content_type="application/pdf")
        response['Content-Disposition'] = f'inline; filename="TRD_{encabezado.oficina_productora}.pdf"'
        return response
    except NameError:
        return HttpResponse("PDF Exporter not found", status=500)

@csrf_exempt
def api_ccd_oficina(request, nombre_oficina):
    try:
        datos = catalogo_ccd.obtener_datos_oficina(nombre_oficina)
        return JsonResponse(datos or {"series": []})
    except NameError:
        return JsonResponse({"series": []})

@csrf_exempt
@require_POST
def api_guardar_ccd_personalizado(request):
    if not is_trd_admin(request.user):
        return JsonResponse({'success': False, 'error': 'Permiso denegado.'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST
        
    oficina = data.get("oficina", "").strip()
    serie_cod = data.get("serie_codigo", "").strip()
    serie_nom = data.get("serie_nombre", "").strip()
    sub_cod = data.get("subserie_codigo", "").strip()
    sub_nom = data.get("subserie_nombre", "").strip()

    if not oficina or not serie_nom:
        return JsonResponse({"ok": False, "error": "Debe proporcionar al menos la oficina y el nombre de la serie."}, status=400)

    try:
        catalogo_ccd.registrar_serie_o_subserie_personalizada(
            nombre_o_prefijo=oficina,
            serie_cod=serie_cod,
            serie_nom=serie_nom,
            sub_cod=sub_cod,
            sub_nom=sub_nom
        )
        datos_actualizados = catalogo_ccd.obtener_datos_oficina(oficina)
        return JsonResponse({"ok": True, "catalogo": datos_actualizados})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

@csrf_exempt
@require_POST
def api_actualizar_ccd(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST
        
    oficina = data.get("oficina", "").strip()
    cod_actual = data.get("codigo_actual", "").strip()
    nuevo_cod = data.get("nuevo_codigo", "").strip()
    nuevo_nom = data.get("nuevo_nombre", "").strip()

    if not oficina or not cod_actual or not nuevo_cod:
        return JsonResponse({"ok": False, "error": "Faltan datos obligatorios para actualizar."}, status=400)

    try:
        ok = catalogo_ccd.actualizar_serie_en_catalogo(oficina, cod_actual, nuevo_cod, nuevo_nom)
        if not ok:
            return JsonResponse({"ok": False, "error": "No se encontró la serie en el catálogo."}, status=404)
        datos_actualizados = catalogo_ccd.obtener_datos_oficina(oficina)
        return JsonResponse({"ok": True, "catalogo": datos_actualizados})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

@csrf_exempt
@require_POST
def api_eliminar_ccd(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST
        
    oficina = data.get("oficina", "").strip()
    cod_serie = data.get("codigo_serie", "").strip()

    if not oficina or not cod_serie:
        return JsonResponse({"ok": False, "error": "Faltan oficina o código de serie a eliminar."}, status=400)

    try:
        catalogo_ccd.eliminar_serie_de_catalogo(oficina, cod_serie)
        datos_actualizados = catalogo_ccd.obtener_datos_oficina(oficina)
        return JsonResponse({"ok": True, "catalogo": datos_actualizados})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

def eliminar_trd(request, enc_id):
    if not is_trd_admin(request.user):
        messages.error(request, 'No tienes permisos para eliminar Tablas de Retención.')
        return redirect('trd:inicio')
    from django.shortcuts import get_object_or_404
    from .models import TRDEncabezado
    try:
        trd = get_object_or_404(TRDEncabezado, id=enc_id)
        nombre = f"{trd.oficina.nombre} (V{trd.version})"
        trd.delete()
        messages.success(request, f'La TRD de {nombre} fue eliminada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar TRD: {str(e)}')
    return redirect('trd:inicio')

def actualizar_encabezado_trd(request, enc_id):
    if not is_trd_admin(request.user):
        messages.error(request, 'No tienes permisos para editar los metadatos de la Tabla de Retención.')
        return redirect('trd:editar_trd', enc_id=enc_id)
        
    if request.method == 'POST':
        from django.shortcuts import get_object_or_404
        from .models import EncabezadoTRD
        
        try:
            enc = get_object_or_404(EncabezadoTRD, id=enc_id)
            enc.entidad_productora = request.POST.get('entidad_productora', enc.entidad_productora).strip()
            enc.fecha_creacion = request.POST.get('fecha_creacion', enc.fecha_creacion).strip()
            enc.fecha_ajuste = request.POST.get('fecha_ajuste', enc.fecha_ajuste).strip()
            enc.fecha_aprobacion = request.POST.get('fecha_aprobacion', enc.fecha_aprobacion).strip()
            enc.fecha_convalidacion = request.POST.get('fecha_convalidacion', enc.fecha_convalidacion).strip()
            enc.responsable_gestion_documental = request.POST.get('resp_gd', enc.responsable_gestion_documental).strip()
            enc.cargo_responsable_gestion_documental = request.POST.get('cargo_gd', enc.cargo_responsable_gestion_documental).strip()
            enc.responsable_area = request.POST.get('resp_area', enc.responsable_area).strip()
            enc.cargo_responsable_area = request.POST.get('cargo_area', enc.cargo_responsable_area).strip()
            enc.superior_jerarquico = request.POST.get('resp_sup', enc.superior_jerarquico).strip()
            enc.cargo_superior_jerarquico = request.POST.get('cargo_sup', enc.cargo_superior_jerarquico).strip()
            enc.version = request.POST.get('version', enc.version).strip()
            enc.estado = request.POST.get('estado', enc.estado).strip()
            enc.vigencia_ano = request.POST.get('vigencia_ano', enc.vigencia_ano).strip()
            enc.save()
            messages.success(request, '¡Los datos principales de la TRD fueron actualizados con éxito!')
        except Exception as e:
            messages.error(request, f'Error al actualizar TRD: {str(e)}')
            
    return redirect('trd:editar_trd', enc_id=enc_id)
