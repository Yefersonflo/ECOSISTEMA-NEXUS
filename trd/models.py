from django.db import models

class EncabezadoTRD(models.Model):
    entidad_productora = models.CharField(max_length=200)
    oficina_productora = models.CharField(max_length=200)
    fecha_creacion = models.CharField(max_length=50, blank=True)
    fecha_ajuste = models.CharField(max_length=50, blank=True)
    fecha_aprobacion = models.CharField(max_length=50, blank=True)
    fecha_convalidacion = models.CharField(max_length=50, blank=True)
    responsable_gestion_documental = models.CharField(max_length=200)
    cargo_responsable_gestion_documental = models.CharField(max_length=200)
    responsable_area = models.CharField(max_length=200, blank=True)
    cargo_responsable_area = models.CharField(max_length=200, blank=True)
    superior_jerarquico = models.CharField(max_length=200)
    cargo_superior_jerarquico = models.CharField(max_length=200)
    version = models.CharField(max_length=50, default="1.0")
    estado = models.CharField(max_length=50, default="VIGENTE")
    vigencia_ano = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.oficina_productora} - {self.estado}"

class ItemTRD(models.Model):
    encabezado = models.ForeignKey(EncabezadoTRD, on_delete=models.CASCADE, related_name='items')
    parent_id = models.IntegerField(null=True, blank=True)
    codigo = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50)
    nombre = models.CharField(max_length=500)
    soporte_papel = models.BooleanField(default=False)
    soporte_electronico = models.BooleanField(default=False)
    extensiones = models.CharField(max_length=200, blank=True)
    retencion_gestion = models.IntegerField(null=True, blank=True)
    retencion_central = models.IntegerField(null=True, blank=True)
    disposicion_final = models.CharField(max_length=10, blank=True)
    reproduccion_tecnica = models.CharField(max_length=50, blank=True)
    procedimiento = models.TextField(blank=True)
    orden = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
