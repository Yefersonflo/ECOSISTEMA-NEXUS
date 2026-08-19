import os
import re
import json
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from afiliados.models import Carpeta

def clean_text(value):
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()

def clean_cedula(value):
    return re.sub(r"\D", "", clean_text(value))

def clean_int(value, default=1, minimum=1, maximum=None):
    text = clean_text(value)
    if not text:
        return default
    match = re.search(r"\d+", text)
    if not match:
        return default
    number = int(match.group(0))
    if number < minimum:
        return default
    if maximum is not None and number > maximum:
        return maximum
    return number

class Command(BaseCommand):
    help = "Migra 1940 expedientes directamente a PostgreSQL de forma incondicional."

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Limpia la tabla antes de importar.")

    def handle(self, *args, **options):
        from django.conf import settings
        base_dir = getattr(settings, 'BASE_DIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        clean_json_path = os.path.join(base_dir, "expedientes_clean.json")
        json_path = os.path.join(base_dir, "expedientes_data.json")

        self.stdout.write(f"Buscando archivos de datos en: {base_dir}")

        raw_records = []
        if os.path.exists(clean_json_path):
            self.stdout.write(self.style.SUCCESS(f"Cargando {clean_json_path}..."))
            with open(clean_json_path, "r", encoding="utf-8") as f:
                raw_records = json.load(f)
        elif os.path.exists(json_path):
            self.stdout.write(self.style.SUCCESS(f"Cargando {json_path}..."))
            with open(json_path, "r", encoding="utf-8") as f:
                raw_records = json.load(f)

        if not raw_records:
            self.stdout.write(self.style.ERROR("No se encontro archivo JSON de datos."))
            return

        self.stdout.write(self.style.SUCCESS(f"Registros encontrados en JSON: {len(raw_records)}"))

        # Borrar registros de trabajadores existentes para garantizar importación limpia y completa
        Carpeta.objects.filter(categoria="TRABAJADOR").delete()
        self.stdout.write("Base de datos de trabajadores limpiada para importacion directa.")

        seen_cedulas = set()
        occupied_locations = set()
        to_create = []
        skipped = 0

        for r in raw_records:
            cedula = clean_cedula(r.get("cedula") or r.get("Cédula"))
            if not cedula or cedula in seen_cedulas:
                skipped += 1
                continue

            seen_cedulas.add(cedula)

            modulo_num = clean_int(r.get("modulo") or r.get("Módulo"))
            estante_num = clean_int(r.get("estante") or r.get("Estante"))
            bandeja_num = clean_int(r.get("bandeja") or r.get("Bandeja"))
            cubiculo_num = clean_int(r.get("cubiculo") or r.get("Cubículo"))
            num_carpeta = clean_int(r.get("numero_carpeta") or r.get("Número de Carpeta"), maximum=55)

            loc_key = (modulo_num, estante_num, bandeja_num, cubiculo_num, num_carpeta)
            while loc_key in occupied_locations:
                num_carpeta = (num_carpeta % 55) + 1
                loc_key = (modulo_num, estante_num, bandeja_num, cubiculo_num, num_carpeta)

            occupied_locations.add(loc_key)

            to_create.append(Carpeta(
                categoria="TRABAJADOR",
                identificacion=cedula,
                nombre=clean_text(r.get("nombre") or r.get("Nombre")).upper() or "SIN NOMBRE",
                fecha=clean_text(r.get("fecha") or r.get("Fecha")),
                tipo_identificacion=clean_text(r.get("tipo_identificacion") or r.get("Tipo Identificación")) or "CC",
                estado=clean_text(r.get("estado") or r.get("Estado")) or "ACTIVO",
                fecha_retiro=clean_text(r.get("fecha_retiro") or r.get("Fecha Retiro")),
                modulo=modulo_num,
                estante=estante_num,
                bandeja=bandeja_num,
                cubiculo=cubiculo_num,
                numero_carpeta=num_carpeta,
            ))

        with transaction.atomic():
            Carpeta.objects.bulk_create(to_create, batch_size=500)

        self.stdout.write(self.style.SUCCESS(
            f"MIGRACION EXITOSA: {len(to_create)} expedientes insertados en PostgreSQL. Omitidos: {skipped}."
        ))
