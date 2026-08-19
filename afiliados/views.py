# Importa el mÃ³dulo os para interactuar con el sistema operativo (rutas, archivos)
import os
import re
import datetime
# Importa uuid para generar identificadores Ãºnicos universales (usado en radicados fÃ­sicos)
import uuid
# Importa funciones Ãºtiles de Django: renderizar templates, obtener objetos seguros y redireccionar
from django.shortcuts import render, get_object_or_404, redirect
# Importa el decorador que exige que un usuario estÃ© logueado para acceder a una vista
from django.contrib.auth.decorators import login_required
# Importa el modelo de Usuario por defecto de Django
from django.contrib.auth.models import User
# Importa el sistema de mensajes de Django para mostrar alertas (Ã©xito, error, etc.)
from django.contrib import messages
# Importa Q para hacer consultas complejas en la base de datos (ej. AND, OR)
from django.db.models import Q
# Importa timezone de Django para manejar fechas con conocimiento de la zona horaria
from django.utils import timezone

# Importa los modelos locales de la aplicaciÃ³n 'afiliados'
from .models import Carpeta, HistorialCarpeta, Profile
# Importa los formularios locales para validación y creación de datos
from .forms import CarpetaForm
# Importa los modelos de la aplicaciÃ³n 'documentos' relacionados con la correspondencia
from documentos.models import Documento, TipoDocumento
# Importa los modelos de la aplicaciÃ³n 'ubicacion' para el manejo fÃ­sico del archivo


# FunciÃ³n auxiliar para determinar si un usuario tiene privilegios mÃ¡ximos
def is_super(user):
    # Retorna True si es superusuario de Django O si su perfil tiene el rol 'SUPER'
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.rol == 'SUPER')

# API pública en formato JSON para consultas remotas del Gestor de Escritorio
from django.http import JsonResponse

def api_buscar_afiliado(request):
    try:
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse({'error': 'Parámetro q requerido'}, status=400)
        
        clean_q = re.sub(r"\D", "", query)
        qs = Carpeta.objects.filter(categoria='TRABAJADOR')
        matches = []
        if clean_q:
            matches = list(qs.filter(Q(identificacion__icontains=clean_q) | Q(nombre__icontains=query))[:50])
        else:
            matches = list(qs.filter(nombre__icontains=query)[:50])
            
        if not matches:
            return JsonResponse({'encontrado': False, 'resultados': [], 'mensaje': 'Expediente no encontrado'}, status=200)
            
        results = []
        for match in matches:
            fecha_str = ""
            if match.fecha:
                fecha_str = str(match.fecha)
            elif getattr(match, 'fecha_registro', None):
                fecha_str = match.fecha_registro.strftime("%Y-%m-%d")

            results.append({
                'Fecha': fecha_str,
                'Tipo Identificación': match.tipo_identificacion or "CC",
                'Cédula': match.identificacion,
                'Nombre': match.nombre or "SIN NOMBRE",
                'Módulo': str(match.modulo),
                'Estante': str(match.estante),
                'Bandeja': str(match.bandeja),
                'Cubículo': str(match.cubiculo),
                'Número de Carpeta': str(match.numero_carpeta),
                'Estado': match.estado or "ACTIVO",
                'Fecha Retiro': match.fecha_retiro or "No aplica"
            })

        response_data = dict(results[0])
        response_data['encontrado'] = True
        response_data['resultados'] = results
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'encontrado': False, 'resultados': [], 'error': str(e)}, status=200)

from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

@csrf_exempt
def api_sincronizar_afiliados(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
        records = data.get('registros', [])
        secret = data.get('secret', '')
        if secret != 'nexus_cloud_sync_secret_2026':
            return JsonResponse({'error': 'No autorizado'}, status=401)
            
        if not records:
            return JsonResponse({'mensaje': 'No hay registros para sincronizar', 'sincronizados': 0})
            
        updated = 0
        with transaction.atomic():
            if data.get('clear'):
                Carpeta.objects.filter(categoria='TRABAJADOR').delete()
                
            for r in records:
                cedula = re.sub(r"\D", "", str(r.get('cedula') or r.get('Cédula') or ''))
                if not cedula:
                    continue
                    
                nombre = str(r.get('nombre') or r.get('Nombre') or 'SIN NOMBRE').upper().strip()
                fecha = str(r.get('fecha') or r.get('Fecha') or '')
                tipo_id = str(r.get('tipo_identificacion') or r.get('Tipo Identificación') or 'CC')
                estado = str(r.get('estado') or r.get('Estado') or 'ACTIVO')
                fecha_retiro = str(r.get('fecha_retiro') or r.get('Fecha Retiro') or '')
                
                existing = Carpeta.objects.filter(identificacion=cedula, categoria='TRABAJADOR').first()
                if existing:
                    existing.nombre = nombre or existing.nombre
                    if fecha: existing.fecha = fecha
                    if estado: existing.estado = estado
                    if fecha_retiro and fecha_retiro.upper() not in ["NO APLICA", "", "NONE", "NAN"]:
                        existing.fecha_retiro = fecha_retiro
                    existing.save()
                    updated += 1
                else:
                    try:
                        modulo = int(r.get('modulo') or r.get('Módulo') or 1)
                        estante = int(r.get('estante') or r.get('Estante') or 1)
                        bandeja = min(max(int(r.get('bandeja') or r.get('Bandeja') or 1), 1), 6)
                        cubiculo = min(max(int(r.get('cubiculo') or r.get('Cubículo') or 1), 1), 6)
                        num_carpeta = min(max(int(r.get('numero_carpeta') or r.get('Número de Carpeta') or 1), 1), 55)
                    except Exception:
                        modulo, estante, bandeja, cubiculo, num_carpeta = 1, 1, 1, 1, 1

                    used_nums = set(Carpeta.objects.filter(categoria='TRABAJADOR', modulo=modulo, estante=estante, bandeja=bandeja, cubiculo=cubiculo).values_list('numero_carpeta', flat=True))
                    while num_carpeta in used_nums and num_carpeta <= 55:
                        num_carpeta += 1
                    if num_carpeta > 55:
                        num_carpeta = (len(used_nums) % 55) + 1

                    Carpeta.objects.create(
                        identificacion=cedula,
                        categoria='TRABAJADOR',
                        nombre=nombre,
                        fecha=fecha,
                        tipo_identificacion=tipo_id,
                        estado=estado,
                        fecha_retiro=fecha_retiro,
                        modulo=modulo,
                        estante=estante,
                        bandeja=bandeja,
                        cubiculo=cubiculo,
                        numero_carpeta=num_carpeta,
                    )
                    updated += 1
                
        return JsonResponse({'exito': True, 'sincronizados': updated})
    except Exception as e:
        return JsonResponse({'exito': False, 'error': str(e)}, status=200)

# Vista del panel principal, requiere inicio de sesiÃ³n
@login_required
def dashboard(request):
    es_admin = is_super(request.user)
    historial = HistorialCarpeta.objects.all().order_by('-fecha')[:10] if es_admin else HistorialCarpeta.objects.filter(usuario=request.user)[:10]

    # Estadísticas para el Dashboard Interactivo
    total_carpetas = Carpeta.objects.count()
    activos_cnt = Carpeta.objects.filter(estado='ACTIVO').count()
    inactivos_cnt = Carpeta.objects.filter(estado='INACTIVO').count()
    muertos_cnt = Carpeta.objects.filter(estado='MUERTO').count()
    
    # Calcular Alertas Naranja (+10 años inactivos)
    hoy = datetime.date.today()
    diez_anos_atras = hoy.year - 10
    alertas_naranja = 0
    
    for c in Carpeta.objects.filter(estado='INACTIVO'):
        fr = str(c.fecha_retiro or '')
        years = re.findall(r'\b(19\d\d|20\d\d)\b', fr)
        if years:
            try:
                y = int(years[0])
                if y <= diez_anos_atras:
                    alertas_naranja += 1
            except Exception:
                pass

    return render(request, 'dashboard/index.html', {
        'total_carpetas': total_carpetas,
        'activos_cnt': activos_cnt,
        'inactivos_cnt': inactivos_cnt,
        'muertos_cnt': muertos_cnt,
        'alertas_naranja': alertas_naranja,
        'es_admin': es_admin,
        'historial': historial,
        'header_title': 'Panel Principal'
    })

# MÓDULOS DE VENTANILLA ÚNICA Y CORRESPONDENCIA DEBAJO ELIMINADOS

# === VISTAS DE GESTIÃƒâ€œN DOCUMENTAL Y ARCHIVO ===

# Vista principal para la administración del archivo físico
@login_required
def gestion_documental(request):
    # Obtiene la categoría actual de la URL (por defecto TRABAJADOR)
    cat_activa = request.GET.get('cat', 'TRABAJADOR')
    # Obtiene el término de búsqueda
    query = request.GET.get('q', '').strip()
    
    # Obtiene todas las carpetas de la categoría seleccionada, ordenadas por fecha de registro (últimas creadas primero)
    carpetas = Carpeta.objects.filter(categoria=cat_activa).order_by('-fecha_registro')
    
    # Si hay una búsqueda activa, filtra por identificación O nombre que contenga el texto
    if query:
        carpetas = carpetas.filter(Q(identificacion__icontains=query) | Q(nombre__icontains=query))
    
    # Paginar las carpetas (25 por página)
    from django.core.paginator import Paginator
    paginator = Paginator(carpetas, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Diccionario con el conteo total de expedientes por categoría
    stats = {
        'trabajadores': Carpeta.objects.filter(categoria='TRABAJADOR').count(),
        'patronales': Carpeta.objects.filter(categoria='PATRONAL').count(),
        'archivos': 0
    }
    
    # Lógica para guardar un nuevo expediente físico
    if request.method == 'POST':
        if not (hasattr(request.user, 'profile') and request.user.profile.rol in ['SUPER', 'JEFE']):
            messages.error(request, "No tiene permisos para registrar nuevos expedientes.")
            return redirect('gestion_documental')
        # Carga los datos del formulario incluyendo archivos (si los hay)
        form = CarpetaForm(request.POST, request.FILES)
        if form.is_valid(): # Valida que los datos sean correctos según el modelo
            try:
                # Guarda la carpeta directamente en la base de datos
                nueva = form.save()
                
                # Alerta de éxito y recarga la página en la misma categoría
                messages.success(request, f"Expediente de {nueva.nombre} registrado.")
                return redirect(f"{request.path}?cat={nueva.categoria}")
            except Exception as e: 
                # Si ocurre un error en base de datos, lo muestra
                messages.error(request, f"Error: {str(e)}")
    else: 
        # Si no es POST, crea un formulario vacío con la categoría actual preseleccionada
        form = CarpetaForm(initial={'categoria': cat_activa})
        
    # Renderiza la interfaz de gestión documental pasando carpetas, estadísticas y formulario
    return render(request, 'afiliados/gestion_documental.html', {
        'cat_activa': cat_activa, 'carpetas': page_obj, 'stats': stats, 'form': form, 'header_title': 'Gestion Documental'
    })

# Vista para ver los detalles de una carpeta física y su contenido
@login_required
def detalle_carpeta(request, carpeta_id):
    # Busca la carpeta por ID
    it = get_object_or_404(Carpeta, id=carpeta_id)
    # Obtiene los documentos asociados
    documentos = it.documentos.all().order_by('-fecha_creacion')
    
    if request.method == 'POST':
        # LÓGICA DE EDICIÓN DE CARPETA
        if 'editar_carpeta' in request.POST:
            if not (hasattr(request.user, 'profile') and request.user.profile.rol in ['SUPER', 'JEFE']):
                messages.error(request, "No tiene permisos para editar expedientes.")
                return redirect('detalle_carpeta', carpeta_id=it.id)
            form = CarpetaForm(request.POST, instance=it)
            if form.is_valid():
                try:
                    actualizada = form.save()
                    
                    # Registrar acción en historial
                    HistorialCarpeta.objects.create(
                        carpeta=it,
                        usuario=request.user,
                        accion='EDICION',
                        observaciones='Se actualizaron los datos del expediente.'
                    )
                    
                    messages.success(request, "Datos del expediente actualizados correctamente.")
                except Exception as e:
                    messages.error(request, f"Error al actualizar: {str(e)}")
            else:
                messages.error(request, "Error en el formulario. Verifique los datos.")
        
        # LÓGICA DE CARGA DE DOCUMENTOS
        elif 'subir_doc' in request.POST:
            nombre_doc = request.POST.get('nombre_doc')
            archivo = request.FILES.get('archivo')
            if nombre_doc and archivo:
                Documento.objects.create(
                    nombre=nombre_doc,
                    archivo=archivo,
                    carpeta=it
                )
                # Registrar carga de documento en historial
                HistorialCarpeta.objects.create(
                    carpeta=it,
                    usuario=request.user,
                    accion='DOCUMENTO',
                    observaciones=f'Se subió el archivo: {nombre_doc}'
                )
                messages.success(request, f"Archivo '{nombre_doc}' subido a la bodega digital.")
            else:
                messages.error(request, "Debe proporcionar un nombre y un archivo.")
        
        return redirect('detalle_carpeta', carpeta_id=it.id)
    
    form = CarpetaForm(instance=it)
    
    # Obtener historial de auditoría de esta carpeta específica (últimos 20 eventos)
    historial_carpeta = HistorialCarpeta.objects.filter(carpeta=it).select_related('usuario').order_by('-fecha')[:20]
    
    return render(request, 'afiliados/detalle.html', {
        'carpeta': it,
        'form': form,
        'documentos': documentos,
        'historial_carpeta': historial_carpeta,
        'header_title': f'Expediente: {it.nombre}'
    })


# Vista para eliminar definitivamente un expediente fÃ­sico del sistema
@login_required
def borrar_carpeta(request, carpeta_id):
    if not is_super(request.user):
        messages.error(request, "No tiene permisos para eliminar expedientes del sistema.")
        return redirect('gestion_documental')
    # Busca la carpeta
    it = get_object_or_404(Carpeta, id=carpeta_id)
    # Guarda el nombre para mostrarlo en el mensaje
    nom = it.nombre
    # Elimina el registro de la base de datos
    it.delete()
    # Muestra un aviso de eliminaciÃ³n
    messages.warning(request, f"Expediente {nom} eliminado.")
    # Regresa al listado principal
    return redirect('gestion_documental')

@login_required
def borrar_documento(request, doc_id):
    if not is_super(request.user):
        from documentos.models import Documento
        it = get_object_or_404(Documento, id=doc_id)
        messages.error(request, "No tiene permisos para eliminar documentos digitales.")
        return redirect('detalle_carpeta', carpeta_id=it.carpeta.id)
        
    # Buscar el documento por su ID y borrarlo
    from documentos.models import Documento
    it = get_object_or_404(Documento, id=doc_id)
    carpeta_id = it.carpeta.id
    it.delete()
    messages.warning(request, "Documento PDF eliminado digitalmente.")
    return redirect('detalle_carpeta', carpeta_id=carpeta_id)

from django.http import HttpResponse
from openpyxl import Workbook

@login_required
def mapa_visual(request):
    nivel = 'CATEGORIA'
    cat = request.GET.get('cat')
    mod_id = request.GET.get('mod')
    est_id = request.GET.get('est')
    ban_id = request.GET.get('ban')
    cub_id = request.GET.get('cub')
    
    objetos = []
    breadcrumb = []
    
    if cat:
        nivel = 'MODULO'
        breadcrumb.append({'nombre': f'Archivo {cat}', 'url': f'?cat={cat}'})
        
        if mod_id:
            nivel = 'ESTANTE'
            breadcrumb.append({'nombre': f'MÃ³dulo {mod_id}', 'url': f'?cat={cat}&mod={mod_id}'})
            
            if est_id:
                nivel = 'BANDEJA'
                breadcrumb.append({'nombre': f'Estante {est_id}', 'url': f'?cat={cat}&mod={mod_id}&est={est_id}'})
                
                if ban_id:
                    nivel = 'CUBICULO'
                    breadcrumb.append({'nombre': f'Bandeja {ban_id}', 'url': f'?cat={cat}&mod={mod_id}&est={est_id}&ban={ban_id}'})
                    
                    if cub_id:
                        nivel = 'CARPETA'
                        breadcrumb.append({'nombre': f'CubÃ­culo {cub_id}', 'url': f'?cat={cat}&mod={mod_id}&est={est_id}&ban={ban_id}&cub={cub_id}'})
                        objetos = Carpeta.objects.filter(categoria=cat, modulo=mod_id, estante=est_id, bandeja=ban_id, cubiculo=cub_id).order_by('numero_carpeta')
                    else:
                        cub_nums = Carpeta.objects.filter(categoria=cat, modulo=mod_id, estante=est_id, bandeja=ban_id).values_list('cubiculo', flat=True).distinct().order_by('cubiculo')
                        objetos = [{'id': num, 'numero': num} for num in cub_nums]
                else:
                    ban_nums = Carpeta.objects.filter(categoria=cat, modulo=mod_id, estante=est_id).values_list('bandeja', flat=True).distinct().order_by('bandeja')
                    objetos = [{'id': num, 'numero': num} for num in ban_nums]
            else:
                est_nums = Carpeta.objects.filter(categoria=cat, modulo=mod_id).values_list('estante', flat=True).distinct().order_by('estante')
                objetos = [{'id': num, 'numero': num} for num in est_nums]
        else:
            mod_nums = Carpeta.objects.filter(categoria=cat).values_list('modulo', flat=True).distinct().order_by('modulo')
            objetos = [{'id': num, 'numero': num} for num in mod_nums]

    return render(request, 'afiliados/mapa_visual.html', {
        'nivel': nivel, 'objetos': objetos, 'breadcrumb': breadcrumb, 'cat': cat
    })

@login_required
def panel_reportes(request):
    c_t = Carpeta.objects.filter(categoria='TRABAJADOR').count()
    c_p = Carpeta.objects.filter(categoria='PATRONAL').count()
    
    # Capacidad teÃ³rica (Ejemplo: cada cubÃ­culo 55 carpetas)
    total_cubiculos_t = Carpeta.objects.filter(categoria='TRABAJADOR').values('modulo', 'estante', 'bandeja', 'cubiculo').distinct().count()
    total_cubiculos_p = Carpeta.objects.filter(categoria='PATRONAL').values('modulo', 'estante', 'bandeja', 'cubiculo').distinct().count()
    
    cap_t = total_cubiculos_t * 55
    cap_p = total_cubiculos_p * 55
    
    stats = {
        'trabajadores': c_t,
        'patronales': c_p,
        'total': c_t + c_p,
        'disp_t': cap_t - c_t if cap_t > c_t else 0,
        'perc_t': round((1 - (c_t/cap_t))*100, 1) if cap_t > 0 else 0,
        'disp_p': cap_p - c_p if cap_p > c_p else 0,
        'perc_p': round((1 - (c_p/cap_p))*100, 1) if cap_p > 0 else 0,
    }
    return render(request, 'afiliados/reportes.html', {'stats': stats})

@login_required
def exportar_excel_archivo(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventario Archivo"
    
    headers = ['CATEGORIA', 'NOMBRE', 'IDENTIFICACION', 'CARPETA #', 'MODULO', 'ESTANTE', 'BANDEJA', 'CUBICULO', 'FECHA REGISTRO']
    ws.append(headers)
    
    for c in Carpeta.objects.all():
        ws.append([
            c.get_categoria_display(),
            c.nombre,
            c.identificacion,
            c.numero_carpeta,
            c.modulo,
            c.estante,
            c.bandeja,
            c.cubiculo,
            c.fecha_registro.strftime('%Y-%m-%d %H:%M')
        ])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Inventario_Archivo.xlsx'
    wb.save(response)
    return response

@login_required
def historial_auditoria(request):
    if not is_super(request.user):
        messages.error(request, "No tiene autorización para ver el historial de auditoría.")
        return redirect('dashboard')

    import re
    from django.db import connection
    from django.core.paginator import Paginator
    
    # 1. Obtener registros de la base de datos (Plataforma Web)
    web_records = []
    for h in HistorialCarpeta.objects.all().select_related('usuario', 'carpeta').order_by('-fecha'):
        web_records.append({
            'fecha': h.fecha,
            'usuario': h.usuario.username,
            'accion': h.accion,
            'detalles': f"Expediente: {h.carpeta.nombre} ({h.carpeta.identificacion}). {h.observaciones or ''}",
            'plataforma': 'Web'
        })
        
    # 2. Obtener registros del archivo de texto (Plataforma Escritorio)
    desktop_records = []
    try:
        db_file = connection.settings_dict['NAME']
        log_file = os.path.join(os.path.dirname(db_file), "historial_cambios.txt")
        if os.path.exists(log_file):
            pattern = re.compile(r"^\[(.*?)\]\s+\[Usuario:\s*(.*?)\]\s+(.*?):\s*(.*)$")
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    match = pattern.match(line)
                    if match:
                        timestamp_str, user, action, details = match.groups()
                        try:
                            dt = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                            dt = timezone.make_aware(dt) if timezone.is_naive(dt) else dt
                        except Exception:
                            dt = timezone.now()
                        desktop_records.append({
                            'fecha': dt,
                            'usuario': user,
                            'accion': action,
                            'detalles': details,
                            'plataforma': 'Escritorio'
                        })
    except Exception as e:
        print(f"Error al leer historial_cambios.txt: {e}")
        
    # 3. Combinar y ordenar por fecha descendente
    all_records = web_records + desktop_records
    all_records.sort(key=lambda x: x['fecha'], reverse=True)
    
    # 4. Aplicar filtros
    plat_filter = request.GET.get('plataforma', 'Todos')
    user_filter = request.GET.get('usuario', '').strip().lower()
    action_filter = request.GET.get('accion', 'Todos')
    q_filter = request.GET.get('q', '').strip().lower()
    
    filtered_records = []
    for r in all_records:
        if plat_filter != 'Todos' and r['plataforma'] != plat_filter:
            continue
        if action_filter != 'Todos' and r['accion'].upper() != action_filter.upper():
            continue
        if user_filter and user_filter not in r['usuario'].lower():
            continue
        if q_filter and q_filter not in r['detalles'].lower():
            continue
        filtered_records.append(r)
        
    # 5. Paginación
    paginator = Paginator(filtered_records, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'afiliados/historial_auditoria.html', {
        'page_obj': page_obj,
        'plat_filter': plat_filter,
        'user_filter': user_filter,
        'action_filter': action_filter,
        'q_filter': q_filter,
        'total_eventos': len(filtered_records),
        'header_title': 'Auditoría Global'
    })

@login_required
def exportar_auditoria_excel(request):
    if not is_super(request.user):
        messages.error(request, "No tiene autorización para exportar auditorías.")
        return redirect('dashboard')

    import re
    from django.db import connection
    
    # 1. Obtener registros de la base de datos (Plataforma Web)
    web_records = []
    for h in HistorialCarpeta.objects.all().select_related('usuario', 'carpeta').order_by('-fecha'):
        web_records.append({
            'fecha': h.fecha,
            'usuario': h.usuario.username,
            'accion': h.accion,
            'detalles': f"Expediente: {h.carpeta.nombre} ({h.carpeta.identificacion}). {h.observaciones or ''}",
            'plataforma': 'Web'
        })
        
    # 2. Obtener registros del archivo de texto (Plataforma Escritorio)
    desktop_records = []
    try:
        db_file = connection.settings_dict['NAME']
        log_file = os.path.join(os.path.dirname(db_file), "historial_cambios.txt")
        if os.path.exists(log_file):
            pattern = re.compile(r"^\[(.*?)\]\s+\[Usuario:\s*(.*?)\]\s+(.*?):\s*(.*)$")
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    match = pattern.match(line)
                    if match:
                        timestamp_str, user, action, details = match.groups()
                        try:
                            dt = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                            dt = timezone.make_aware(dt) if timezone.is_naive(dt) else dt
                        except Exception:
                            dt = timezone.now()
                        desktop_records.append({
                            'fecha': dt,
                            'usuario': user,
                            'accion': action,
                            'detalles': details,
                            'plataforma': 'Escritorio'
                        })
    except Exception as e:
        print(f"Error al leer historial_cambios.txt: {e}")
        
    # 3. Combinar y ordenar por fecha descendente
    all_records = web_records + desktop_records
    all_records.sort(key=lambda x: x['fecha'], reverse=True)
    
    # 4. Aplicar filtros
    plat_filter = request.GET.get('plataforma', 'Todos')
    user_filter = request.GET.get('usuario', '').strip().lower()
    action_filter = request.GET.get('accion', 'Todos')
    q_filter = request.GET.get('q', '').strip().lower()
    
    filtered_records = []
    for r in all_records:
        if plat_filter != 'Todos' and r['plataforma'] != plat_filter:
            continue
        if action_filter != 'Todos' and r['accion'].upper() != action_filter.upper():
            continue
        if user_filter and user_filter not in r['usuario'].lower():
            continue
        if q_filter and q_filter not in r['detalles'].lower():
            continue
        filtered_records.append(r)
        
    # 5. Generar Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Historial Auditoria Global"
    
    headers = ['FECHA/HORA', 'PLATAFORMA', 'USUARIO', 'ACCIÓN', 'DETALLES DE EVENTO']
    ws.append(headers)
    
    for r in filtered_records:
        fecha_str = r['fecha'].strftime('%Y-%m-%d %H:%M:%S')
        ws.append([
            fecha_str,
            r['plataforma'],
            r['usuario'],
            r['accion'],
            r['detalles']
        ])
        
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte_Auditoria_Global.xlsx'
    wb.save(response)
    return response

# FIN DE VISTAS DE AFILIADOS

