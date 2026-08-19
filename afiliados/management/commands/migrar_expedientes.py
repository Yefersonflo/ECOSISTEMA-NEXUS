import os
import re
import json
import sqlite3
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
    help = "Migra expedientes hacia PostgreSQL."

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Limpia la tabla antes de importar.")

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        clean_json_path = os.path.join(base_dir, "expedientes_clean.json")
        json_path = os.path.join(base_dir, "expedientes_data.json")

        records = []
        if os.path.exists(clean_json_path):
            self.stdout.write(self.style.SUCCESS(f"Leyendo: {clean_json_path}"))
            with open(clean_json_path, "r", encoding="utf-8") as f:
                raw_records = json.load(f)
            for r in raw_records:
                records.append({
                    "Cédula": r.get("cedula") or r.get("Cédula"),
                    "Nombre": r.get("nombre") or r.get("Nombre"),
                    "Fecha": r.get("fecha") or r.get("Fecha"),
                    "Tipo Identificación": r.get("tipo_identificacion") or r.get("Tipo Identificación"),
                    "Módulo": r.get("modulo") or r.get("Módulo"),
                    "Estante": r.get("estante") or r.get("Estante"),
                    "Bandeja": r.get("bandeja") or r.get("Bandeja"),
                    "Cubículo": r.get("cubiculo") or r.get("Cubículo"),
                    "Número de Carpeta": r.get("numero_carpeta") or r.get("Número de Carpeta"),
                    "Estado": r.get("estado") or r.get("Estado"),
                    "Fecha Retiro": r.get("fecha_retiro") or r.get("Fecha Retiro"),
                })
        elif os.path.exists(json_path):
            self.stdout.write(self.style.SUCCESS(f"Leyendo: {json_path}"))
            with open(json_path, "r", encoding="utf-8") as f:
                records = json.load(f)

        if not records:
            self.stdout.write(self.style.ERROR("No se encontraron registros para migrar."))
            return

        self.stdout.write(self.style.SUCCESS(f"Total registros a procesar: {len(records)}"))

        # Obtener ubicaciones ya usadas en la BD para evitar duplicados
        existing_locs = set(
            Carpeta.objects.filter(categoria="TRABAJADOR").values_list(
                "modulo", "estante", "bandeja", "cubiculo", "numero_carpeta"
            )
        )
        occupied_locations = set(existing_locs)

        created = 0
        skipped = 0
        to_create = []

        with transaction.atomic():
            if options.get("clear"):
                Carpeta.objects.filter(categoria="TRABAJADOR").delete()
                occupied_locations.clear()
                self.stdout.write("Tabla limpiada exitosamente.")

            for r in records:
                cedula = clean_cedula(r.get("Cédula"))
                if not cedula:
                    skipped += 1
                    continue

                # Evitar duplicados por identificacion
                if Carpeta.objects.filter(identificacion=cedula, categoria="TRABAJADOR").exists():
                    skipped += 1
                    continue

                modulo_num = clean_int(r.get("Módulo"))
                estante_num = clean_int(r.get("Estante"))
                bandeja_num = clean_int(r.get("Bandeja"))
                cubiculo_num = clean_int(r.get("Cubículo"))
                num_carpeta = clean_int(r.get("Número de Carpeta"), maximum=55)

                loc_key = (modulo_num, estante_num, bandeja_num, cubiculo_num, num_carpeta)
                while loc_key in occupied_locations:
                    num_carpeta = (num_carpeta % 55) + 1
                    loc_key = (modulo_num, estante_num, bandeja_num, cubiculo_num, num_carpeta)

                occupied_locations.add(loc_key)

                defaults = {
                    "categoria": "TRABAJADOR",
                    "identificacion": cedula,
                    "nombre": clean_text(r.get("Nombre")).upper() or "SIN NOMBRE",
                    "fecha": clean_text(r.get("Fecha")),
                    "tipo_identificacion": clean_text(r.get("Tipo Identificación")) or "CC",
                    "estado": clean_text(r.get("Estado")) or "ACTIVO",
                    "fecha_retiro": clean_text(r.get("Fecha Retiro")),
                    "modulo": modulo_num,
                    "estante": estante_num,
                    "bandeja": bandeja_num,
                    "cubiculo": cubiculo_num,
                    "numero_carpeta": num_carpeta,
                }

                to_create.append(Carpeta(**defaults))
                created += 1

            if to_create:
                Carpeta.objects.bulk_create(to_create, batch_size=500)

        self.stdout.write(self.style.SUCCESS(
            f"MIGRACION A POSTGRESQL FINALIZADA. {created} expedientes insertados. Omitidos: {skipped}."
        ))
