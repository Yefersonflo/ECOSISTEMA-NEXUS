from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Modelo que extiende la información del usuario de Django con roles y perfiles
class Profile(models.Model):
    ROLES = [
        ('SUPER', 'Administrador Total'),
        ('JEFE', 'Jefe de Archivo'),
        ('AUX', 'Auxiliar de Registro y Digitalización'),
        ('USER', 'Usuario Consulta')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rol = models.CharField(max_length=20, choices=ROLES, default='USER')
    acceso_web = models.BooleanField(default=False)
    def __str__(self): return f"{self.user.username} - {self.get_rol_display()}"

import datetime
from django.db import connection

# Modelo que representa las carpetas físicas almacenadas
class Carpeta(models.Model):
    CATEGORIAS = [('TRABAJADOR', 'Trabajadores'), ('PATRONAL', 'Patronales')]
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='TRABAJADOR')
    nombre = models.CharField(max_length=255)
    fecha = models.CharField(max_length=50, blank=True, null=True)
    tipo_identificacion = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    fecha_retiro = models.CharField(max_length=50, blank=True, null=True)
    identificacion = models.CharField(max_length=50)
    
    # Nuevos campos planos de ubicación con validaciones físicas de rango
    modulo = models.PositiveIntegerField(default=1)
    estante = models.PositiveIntegerField(default=1)
    bandeja = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    cubiculo = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    numero_carpeta = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(55)]
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['categoria', 'modulo', 'estante', 'bandeja', 'cubiculo', 'numero_carpeta']
        
    def __str__(self): return f"{self.get_categoria_display()} - {self.nombre}"

    def save(self, *args, **kwargs):
        if self.nombre:
            self.nombre = self.nombre.upper().strip()
        if self.estado:
            self.estado = self.estado.upper().strip()
        if self.tipo_identificacion:
            self.tipo_identificacion = self.tipo_identificacion.upper().strip()

        original_identificacion = None
        if self.pk:
            try:
                orig = Carpeta.objects.get(pk=self.pk)
                original_identificacion = orig.identificacion
            except Exception:
                pass

        super().save(*args, **kwargs)

        if connection.vendor == 'sqlite':
            try:
                modulo_val = str(self.modulo)
                estante_val = str(self.estante)
                bandeja_val = str(self.bandeja)
                cubiculo_val = str(self.cubiculo)
                num_carpeta_val = str(self.numero_carpeta)
                fecha_val = self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S") if getattr(self, 'fecha_registro', None) else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                with connection.cursor() as cursor:
                    if original_identificacion and original_identificacion != self.identificacion:
                        cursor.execute('DELETE FROM expedientes WHERE "Cédula" = %s', [original_identificacion])

                    cursor.execute('INSERT OR REPLACE INTO expedientes ("Fecha", "Tipo Identificación", "Cédula", "Nombre", "Módulo", "Estante", "Bandeja", "Cubículo", "Número de Carpeta", "Estado", "Fecha Retiro") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (self.fecha or fecha_val, self.tipo_identificacion or "CC", self.identificacion, self.nombre.upper(), modulo_val, estante_val, bandeja_val, cubiculo_val, num_carpeta_val, self.estado or "ACTIVO", self.fecha_retiro or ""))
            except Exception:
                pass

        try:
            from .excel_sync import sync_to_excel
            record_data = {
                "Fecha": self.fecha or (self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S") if getattr(self, 'fecha_registro', None) else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "Tipo Identificación": self.tipo_identificacion or "CC",
                "Cédula": self.identificacion,
                "Nombre": self.nombre.upper(),
                "Módulo": str(self.modulo),
                "Estante": str(self.estante),
                "Bandeja": str(self.bandeja),
                "Cubículo": str(self.cubiculo),
                "Número de Carpeta": str(self.numero_carpeta),
                "Estado": self.estado or "ACTIVO",
                "Fecha Retiro": self.fecha_retiro or ""
            }
            sync_to_excel("SAVE", record_data, original_cedula=original_identificacion)
        except Exception:
            pass

    def delete(self, *args, **kwargs):
        identificacion = self.identificacion
        super().delete(*args, **kwargs)
        if connection.vendor == 'sqlite':
            try:
                with connection.cursor() as cursor:
                    cursor.execute('DELETE FROM expedientes WHERE "Cédula" = %s', [identificacion])
            except Exception:
                pass


        try:
            from .excel_sync import sync_to_excel
            sync_to_excel("DELETE", {"Cédula": identificacion})
        except Exception:
            pass

# Modelo para registrar el historial de acciones realizadas sobre las carpetas
class HistorialCarpeta(models.Model):
    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)


# Modelo para rastrear sesiones activas y presencia en tiempo real
class ActiveUserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='active_sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    login_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sesión Activa'
        verbose_name_plural = 'Sesiones Activas'
        ordering = ['-last_activity']

    def is_online(self):
        from django.utils import timezone
        return (timezone.now() - self.last_activity).total_seconds() < 300  # < 5 minutos activo

    def get_device(self):
        ua = str(self.user_agent or "").lower()
        if "windows" in ua:
            os_name = "Windows"
        elif "mac" in ua or "darwin" in ua:
            os_name = "macOS"
        elif "android" in ua:
            os_name = "Android"
        elif "iphone" in ua or "ipad" in ua:
            os_name = "iOS"
        elif "linux" in ua:
            os_name = "Linux"
        else:
            os_name = "PC / Dispositivo"

        if "edg" in ua:
            browser = "Microsoft Edge"
        elif "chrome" in ua:
            browser = "Google Chrome"
        elif "firefox" in ua:
            browser = "Mozilla Firefox"
        elif "safari" in ua and "chrome" not in ua:
            browser = "Apple Safari"
        else:
            browser = "Navegador Web"

        return f"{os_name} • {browser}"


# Modelo para registrar el historial completo de inicios de sesión
class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='login_logs')
    username_entered = models.CharField(max_length=150)
    success = models.BooleanField(default=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Historial de Inicio de Sesión'
        verbose_name_plural = 'Historial de Inicios de Sesión'
        ordering = ['-timestamp']
