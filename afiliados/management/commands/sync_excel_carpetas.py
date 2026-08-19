import os
import re

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from afiliados.excel_sync import COLUMNS, load_shared_folder_path
from afiliados.models import Carpeta



def clean_text(value):
    if value is None:
        return ""
    if pd.isna(value):
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
    help = "Sincroniza a archivo_caja las carpetas de trabajadores desde los Excel particionados de Nexus."

    def add_arguments(self, parser):
        parser.add_argument("--folder", default=None, help="Ruta de la carpeta con 00.xlsx a 99.xlsx.")
        parser.add_argument("--clear-workers", action="store_true", help="Borra trabajadores antes de importar.")

    def handle(self, *args, **options):
        folder = options["folder"] or load_shared_folder_path()
        if not os.path.isdir(folder):
            raise SystemExit(f"Carpeta Excel no encontrada: {folder}")

        files = sorted(
            name for name in os.listdir(folder)
            if re.match(r"^\d{2}\.xlsx$", name, re.IGNORECASE)
        )
        if not files:
            self.stdout.write(self.style.WARNING(f"No se encontraron Excel particionados en {folder}"))
            return

        to_create = []
        created = 0
        updated = 0
        skipped = 0

        with transaction.atomic():
            if options["clear_workers"]:
                deleted, _ = Carpeta.objects.filter(categoria="TRABAJADOR").delete()
                self.stdout.write(f"Trabajadores borrados antes de importar: {deleted}")

            for filename in files:
                path = os.path.join(folder, filename)
                try:
                    df = pd.read_excel(path, dtype=str).fillna("")
                except Exception as exc:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(f"No se pudo leer {filename}: {exc}"))
                    continue

                for col in COLUMNS:
                    if col not in df.columns:
                        df[col] = ""

                for _, row in df.iterrows():
                    cedula = clean_cedula(row.get("Cédula"))
                    if not cedula:
                        skipped += 1
                        continue

                    modulo_num = clean_int(row.get("Módulo"))
                    estante_num = clean_int(row.get("Estante"))
                    bandeja_num = clean_int(row.get("Bandeja"))
                    cubiculo_num = clean_int(row.get("Cubículo"))
                    numero_carpeta = clean_int(row.get("Número de Carpeta"), maximum=55)

                    
                    
                    
                    

                    defaults = {
                        "categoria": "TRABAJADOR",
                        "nombre": clean_text(row.get("Nombre")).upper() or "SIN NOMBRE",
                        "fecha": clean_text(row.get("Fecha")),
                        "tipo_identificacion": clean_text(row.get("Tipo Identificación")) or "CC",
                        "estado": clean_text(row.get("Estado")) or "ACTIVO",
                        "fecha_retiro": clean_text(row.get("Fecha Retiro")),
                        "modulo": modulo_num,
                        "estante": estante_num,
                        "bandeja": bandeja_num,
                        "cubiculo": cubiculo_num,
                        "numero_carpeta": numero_carpeta,
                    }

                    qs = Carpeta.objects.filter(identificacion=cedula, categoria="TRABAJADOR")
                    if qs.exists():
                        # Si ya existe, no sobrescribimos campos que el usuario ya haya corregido o completado.
                        # Solo actualizamos si el campo en base de datos está vacío o tiene valores por defecto.
                        existing = qs.first()
                        update_fields = {}
                        for key, val in defaults.items():
                            existing_val = str(getattr(existing, key, "")).strip()
                            if not existing_val or existing_val == "SIN NOMBRE" or existing_val == "No aplica":
                                update_fields[key] = val
                        
                        if update_fields:
                            qs.update(**update_fields)
                        updated += 1
                    else:
                        if Carpeta.objects.filter(
                            categoria="TRABAJADOR",
                            modulo=modulo_num,
                            estante=estante_num,
                            bandeja=bandeja_num,
                            cubiculo=cubiculo_num,
                            numero_carpeta=numero_carpeta,
                        ).exists() or any(
                            item.categoria == "TRABAJADOR"
                            and item.modulo == modulo_num
                            and item.estante == estante_num
                            and item.bandeja == bandeja_num
                            and item.cubiculo == cubiculo_num
                            and item.numero_carpeta == numero_carpeta
                            for item in to_create
                        ):
                            skipped += 1
                            continue
                        to_create.append(Carpeta(identificacion=cedula, **defaults))
                        created += 1

            if to_create:
                Carpeta.objects.bulk_create(to_create, batch_size=500)

        self.stdout.write(self.style.SUCCESS(
            f"Sincronizacion terminada. Creados: {created}. Actualizados: {updated}. Omitidos: {skipped}."
        ))
