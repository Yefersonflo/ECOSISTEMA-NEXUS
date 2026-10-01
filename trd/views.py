import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EncabezadoTRD, ItemTRD
from .utils.dataclasses_models import EncabezadoTRD as DataEncabezado, ItemTRD as DataItem
from .utils.pdf_exporter import generar_pdf
from .utils.exporter import generar_xlsx

@csrf_exempt
def diligenciar_trd(request):
    if request.method == 'GET':
        return render(request, 'trd/diligenciar.html')
    
    if request.method == 'POST':
        # Assuming the JS sends JSON
        try:
            data = json.loads(request.body)
            enc_data = data.get('encabezado', {})
            items_data = data.get('items', [])
            
            # Save to DB
            enc = EncabezadoTRD.objects.create(
                entidad_productora=enc_data.get('entidad', ''),
                oficina_productora=enc_data.get('oficina', ''),
                responsable_gestion_documental=enc_data.get('responsable_gd_nombre', ''),
                cargo_responsable_gestion_documental=enc_data.get('responsable_gd_cargo', ''),
                responsable_area=enc_data.get('responsable_area_nombre', ''),
                cargo_responsable_area=enc_data.get('responsable_area_cargo', ''),
                superior_jerarquico=enc_data.get('superior_nombre', ''),
                cargo_superior_jerarquico=enc_data.get('superior_cargo', '')
            )
            
            for item in items_data:
                ItemTRD.objects.create(
                    encabezado=enc,
                    codigo=item.get('codigo', ''),
                    nivel=item.get('nivel', ''),
                    nombre=item.get('nombre', ''),
                    soporte_papel=bool(item.get('soporte_papel')),
                    soporte_electronico=bool(item.get('soporte_electronico')),
                    retencion_gestion=int(item.get('retencion_gestion')) if item.get('retencion_gestion') else None,
                    retencion_central=int(item.get('retencion_central')) if item.get('retencion_central') else None,
                    disposicion_final=item.get('disposicion_final', ''),
                    reproduccion_tecnica=item.get('reproduccion_tecnica', ''),
                    procedimiento=item.get('procedimiento', ''),
                    orden=int(item.get('orden', 0))
                )
                
            return JsonResponse({"status": "success", "encabezado_id": enc.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt
def exportar_trd(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        formato = data.get('formato', 'pdf')
        
        # We can either fetch from DB using an ID, or parse the incoming JSON directly like the Flask app did!
        # The Flask app received the full JSON and exported it on the fly!
        enc_data = data.get('encabezado', {})
        items_data = data.get('items', [])
        
        enc_dataclass = DataEncabezado(
            id=1,
            entidad_productora=enc_data.get('entidad', ''),
            oficina_productora=enc_data.get('oficina', ''),
            fecha_creacion='', fecha_ajuste='', fecha_aprobacion='', fecha_convalidacion='',
            responsable_gestion_documental=enc_data.get('responsable_gd_nombre', ''),
            cargo_responsable_gestion_documental=enc_data.get('responsable_gd_cargo', ''),
            responsable_area=enc_data.get('responsable_area_nombre', ''),
            cargo_responsable_area=enc_data.get('responsable_area_cargo', ''),
            superior_jerarquico=enc_data.get('superior_nombre', ''),
            cargo_superior_jerarquico=enc_data.get('superior_cargo', ''),
            version="1.0", estado="VIGENTE", vigencia_ano=""
        )
        
        items_dataclasses = []
        for i, item in enumerate(items_data):
            items_dataclasses.append(DataItem(
                id=i+1,
                encabezado_id=1,
                parent_id=None,
                codigo=item.get('codigo', ''),
                nivel=item.get('nivel', ''),
                nombre=item.get('nombre', ''),
                soporte_papel=bool(item.get('soporte_papel')),
                soporte_electronico=bool(item.get('soporte_electronico')),
                extensiones='',
                retencion_gestion=int(item.get('retencion_gestion')) if item.get('retencion_gestion') else None,
                retencion_central=int(item.get('retencion_central')) if item.get('retencion_central') else None,
                disposicion_final=item.get('disposicion_final', ''),
                reproduccion_tecnica=item.get('reproduccion_tecnica', ''),
                procedimiento=item.get('procedimiento', ''),
                orden=int(item.get('orden', 0))
            ))
            
        if formato == 'pdf':
            buffer = generar_pdf(enc_dataclass, items_dataclasses)
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="TRD.pdf"'
            return response
        elif formato == 'excel':
            buffer = generar_xlsx(enc_dataclass, items_dataclasses)
            response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="TRD.xlsx"'
            return response
            
    return JsonResponse({"error": "Invalid request"}, status=400)
