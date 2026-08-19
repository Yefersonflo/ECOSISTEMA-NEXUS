from django.shortcuts import render, get_object_or_404, redirect
from afiliados.models import Carpeta
from .models import Documento

# Vista para buscar un afiliado por su número de identificación
def buscar_afiliado(request):
    # Procesa la búsqueda cuando se envía el formulario vía POST
    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')

        try:
            # Intenta obtener la carpeta asociada a la identificación proporcionada
            carpeta = Carpeta.objects.get(identificacion=identificacion)
            # Renderiza el resultado si se encuentra la carpeta
            return render(request, 'documentos/resultado.html', {'carpeta': carpeta})
        except Carpeta.DoesNotExist:
            # Muestra una página de error si el afiliado no está registrado
            return render(request, 'documentos/no_existe.html', {'identificacion': identificacion})

    # Renderiza el formulario de búsqueda inicial (GET)
    return render(request, 'documentos/buscar.html')

# Vista para adjuntar un nuevo documento digital a una carpeta específica
def agregar_documento(request, carpeta_id):
    # Obtiene la carpeta por su ID o devuelve 404 si no existe
    carpeta = get_object_or_404(Carpeta, id=carpeta_id)

    # Procesa la carga del archivo cuando se envía el formulario
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        archivo = request.FILES.get('archivo')

        # Valida que se haya subido un archivo y que sea de formato PDF
        if archivo and archivo.name.endswith('.pdf'):
            # Crea el registro del documento asociado a la carpeta
            Documento.objects.create(
                nombre=nombre,
                archivo=archivo,
                carpeta=carpeta
            )
            # Redirige a la vista de búsqueda tras una carga exitosa
            return redirect('buscar')

    # Renderiza el formulario de carga de documentos
    return render(request, 'documentos/agregar.html', {'carpeta': carpeta})

# Create your views here.