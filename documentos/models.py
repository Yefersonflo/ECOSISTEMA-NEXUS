import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

def ruta_documento(instance, filename):
    categoria = instance.carpeta.categoria.lower()
    identificacion = instance.carpeta.identificacion
    return f'documentos/{categoria}/{identificacion}/{filename}'

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    orden = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.nombre
        
    class Meta:
        ordering = ['orden', 'nombre']
        db_table = 'documentos_tipodocumento'

class Documento(models.Model):
    nombre = models.CharField(max_length=255)
    tipos = models.ManyToManyField(TipoDocumento, db_table='documentos_documento_tipos')
    archivo = models.FileField(
        upload_to=ruta_documento,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    carpeta = models.ForeignKey('afiliados.Carpeta', on_delete=models.CASCADE, related_name='documentos')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_subidos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tipo_archivo = models.CharField(max_length=10, editable=False)
    tamano = models.PositiveIntegerField(editable=False)
    comentarios = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.archivo:
            self.tipo_archivo = os.path.splitext(self.archivo.name)[1].lower().replace('.', '')
            try:
                self.tamano = self.archivo.size
            except:
                pass
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'documentos_documento'
