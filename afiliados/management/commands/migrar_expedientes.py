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
    help = "Migra expedientes desde expedientes_data.json o base_datos.db local hacia PostgreSQL."

    def add_arguments(self, parser):
        parser.add_argument("--sqlite-db", default=None, help="Ruta al archivo base_datos.db local.")
        parser.add_argument("--clear", action="store_true", help="Limpia la tabla de carpetas antes de importar.")

    def handle(self, *args, **options):
        db_path = options["sqlite_db"]
        if not db_path:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            possible_path = os.path.join(desktop, "ECOSISTEMA NEXUS", "5. Base de Datos", "base_datos_prueba", "base_datos.db")
            if os.path.exists(possible_path):
                db_path = possible_path

        records = []
        json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "expedientes_data.json")
        
        if os.path.exists(json_path):
            self.stdout.write(self.style.SUCCESS(f"Leyendo archivo de datos expedientes_data.json: {json_path}"))
            with open(json_path, "r", encoding="utf-8") as f:
                records = json.load(f)
            self.stdout.write(self.style.SUCCESS(f"Total registros cargados de JSON: {len(records)}"))
        elif db_path and os.path.exists(db_path):
            self.stdout.write(self.style.SUCCESS(f"Leyendo base de datos local SQLite: {db_path}"))
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM expedientes')
            rows = cursor.fetchall()
            for r in rows:
                records.append({
                    "Cédula": r["Cédula"],
                    "Nombre": r["Nombre"],
                    "Fecha": r["Fecha"],
                    "Tipo Identificación": r["Tipo Identificación"],
                    "Módulo": r["Módulo"],
                    "Estante": r["Estante"],
                    "Bandeja": r["Bandeja"],
                    "Cubículo": r["Cubículo"],
                    "Número de Carpeta": r["Número de Carpeta"],
                    "Estado": r["Estado"],
                    "Fecha Retiro": r["Fecha Retiro"]
                })
            conn.close()
            self.stdout.write(self.style.SUCCESS(f"Total registros leidos de SQLite: {len(records)}"))
        else:
            self.stdout.write(self.style.WARNING("No se encontro ni JSON ni SQLite local."))

        if not records:
            self.stdout.write(self.style.ERROR("No hay registros para migrar."))
            return

        created = 0
        skipped = 0
        to_create = []
        occupied_locations = set()

        with transaction.atomic():
            if options["clear"]:
                Carpeta.objects.filter(categoria="TRABAJADOR").delete()
                self.stdout.write("Base de datos limpiada.")

            for r in records:
                cedula = clean_cedula(r["Cédula"])
                if not cedula:
                    skipped += 1
                    continue

                modulo_num = clean_int(r["Módulo"])
                estante_num = clean_int(r["Estante"])
                bandeja_num = clean_int(r["Bandeja"])
                cubiculo_num = clean_int(r["Cubículo"])
                num_carpeta = clean_int(r["Número de Carpeta"], maximum=55)

                loc_key = (modulo_num, estante_num, bandeja_num, cubiculo_num, num_carpeta)
                if loc_key in occupied_locations:
                    num_carpeta = (num_carpeta % 55) + 1
                    loc_key = (modulo_num, estante_num, bandeja_num, cubiculo_num, num_carpeta)

                occupied_locations.add(loc_key)

                defaults = {
                    "categoria": "TRABAJADOR",
                    "identificacion": cedula,
                    "nombre": clean_text(r["Nombre"]).upper() or "SIN NOMBRE",
                    "fecha": clean_text(r["Fecha"]),
                    "tipo_identificacion": clean_text(r["Tipo Identificación"]) or "CC",
                    "estado": clean_text(r["Estado"]) or "ACTIVO",
                    "fecha_retiro": clean_text(r["Fecha Retiro"]),
                    "modulo": modulo_num,
                    "estante": estante_num,
                    "bandeja": bandeja_num,
                    "cubiculo": cubiculo_num,
                    "numero_carpeta": num_carpeta,
                }

                to_create.append(Carpeta(**defaults))
                created += 1

            if to_create:
                Carpeta.objects.bulk_create(to_create, batch_size=500, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(
            f"MIGRACION A POSTGRESQL FINALIZADA. {created} expedientes subidos a la nube. Omitidos: {skipped}."
        ))
