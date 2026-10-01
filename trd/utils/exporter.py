"""Exportador al formato oficial PADO308-PR004-FADO004 v2.0 en Excel.

Utiliza como base la plantilla institucional oficial `assets/FORMATOS_GD.xlsx` (hoja `FADO-004`),
diligenciando la oficina productora, las series/subseries/tipos documentales,
los responsables, las fechas y manteniendo el instructivo oficial intacto.
"""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Iterable

import openpyxl
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.styles import Alignment, Border, Font, Side

from .dataclasses_models import (
    CODIGO_FORMATO,
    NIVEL_SERIE,
    NIVEL_SUBSERIE,
    NIVEL_TIPO,
    VERSION_FORMATO,
    EncabezadoTRD,
    ItemTRD,
)

ASSETS = Path(__file__).resolve().parent.parent / "assets"
PLANTILLA_EXCEL = ASSETS / "FORMATOS_GD.xlsx"


def generar_xlsx(encabezado: EncabezadoTRD, items: Iterable[ItemTRD]) -> BytesIO:
    """Construye el libro Excel basado en la plantilla oficial FADO-004."""
    if PLANTILLA_EXCEL.exists():
        wb = openpyxl.load_workbook(PLANTILLA_EXCEL, rich_text=True)
    else:
        wb = openpyxl.load_workbook(r"C:\Users\YEFERSON\Downloads\FORMATOS GD.xlsx", rich_text=True)

    # Conservar únicamente la hoja oficial FADO-004
    for name in wb.sheetnames:
        if name != "FADO-004":
            del wb[name]

    ws = wb["FADO-004"]
    ws.title = "FADO-004"

    # 1. Encabezado institucional con texto enriquecido
    ws["A6"] = f"OFICINA PRODUCTORA: {encabezado.oficina_productora.upper()}"

    f_bold_9 = InlineFont(rFont="Tahoma", sz=9, b=True)
    f_norm_9 = InlineFont(rFont="Tahoma", sz=9, b=False)
    f_bold_10 = InlineFont(rFont="Tahoma", sz=10, b=True)
    f_norm_10 = InlineFont(rFont="Tahoma", sz=10, b=False)

    ws["L2"] = CellRichText([
        TextBlock(f_bold_9, "CÓDIGO: "),
        TextBlock(f_norm_9, CODIGO_FORMATO),
    ])
    ws["L3"] = CellRichText([
        TextBlock(f_bold_10, "Fecha creación \n"),
        TextBlock(f_norm_10, encabezado.fecha_creacion or "02/01/2012"),
    ])
    ws["M3"] = CellRichText([
        TextBlock(f_bold_10, "Fecha ajuste \n"),
        TextBlock(f_norm_10, encabezado.fecha_ajuste or "30/08/2024"),
    ])
    ws["L4"] = CellRichText([
        TextBlock(f_bold_9, "Versión: "),
        TextBlock(f_norm_9, VERSION_FORMATO),
    ])

    # 2. Preparar filas para los items de la TRD
    lista_items = list(items)
    n_items = len(lista_items)
    filas_base_plantilla = 18  # Filas 14 a 31 en la plantilla vacía
    delta = max(0, n_items - filas_base_plantilla)

    if delta > 0:
        # Desplazar celdas combinadas de firmas, fechas e instructivo
        for m in list(ws.merged_cells.ranges):
            if m.min_row >= 32:
                r_min, r_max, c_min, c_max = m.min_row, m.max_row, m.min_col, m.max_col
                ws.unmerge_cells(str(m))
                ws.merge_cells(start_row=r_min + delta, start_column=c_min,
                               end_row=r_max + delta, end_column=c_max)
        ws.insert_rows(32, delta)

    thin = Side(style="thin", color="000000")

    font_bold = Font(name="Tahoma", size=8, bold=True)
    font_normal = Font(name="Tahoma", size=8, bold=False)

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # Identificar qué subseries son la 2da o posterior dentro de su serie
    subseries_por_serie_count = 0
    es_segunda_o_mas_subserie = []
    for item in lista_items:
        if item.nivel == NIVEL_SERIE:
            subseries_por_serie_count = 0
            es_segunda_o_mas_subserie.append(False)
        elif item.nivel == NIVEL_SUBSERIE:
            subseries_por_serie_count += 1
            es_segunda_o_mas_subserie.append(subseries_por_serie_count > 1)
        else:
            es_segunda_o_mas_subserie.append(False)

    alturas_nom = {}
    lineas_proc_dict = {}
    for i, item in enumerate(lista_items):
        r = 14 + i
        # Asegurar combinación de celdas B:C (siempre por fila)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        # La combinación de L:M se hará por grupos al final del loop

        # Bordes: Líneas negras completas en columnas
        # Línea horizontal divisoria:
        # - Al inicio de la tabla (i == 0)
        # - Al iniciar una nueva SERIE (item.nivel == NIVEL_SERIE)
        # - A partir de la 2da subserie en adelante (es_segunda_o_mas_subserie[i])
        b_top = thin if (i == 0 or item.nivel == NIVEL_SERIE or es_segunda_o_mas_subserie[i]) else None
        
        es_ultimo = (i == n_items - 1)
        siguiente_es_serie = (not es_ultimo and lista_items[i + 1].nivel == NIVEL_SERIE)
        siguiente_es_subserie_divisoria = (not es_ultimo and es_segunda_o_mas_subserie[i + 1])
        b_bottom = thin if (es_ultimo or siguiente_es_serie or siguiente_es_subserie_divisoria) else None
        
        cell_border = Border(left=thin, right=thin, top=b_top, bottom=b_bottom)

        for col in range(1, 14):
            ws.cell(row=r, column=col).border = cell_border

        # Columna A: Código alineado a la izquierda (solo series y subseries)
        cA = ws.cell(row=r, column=1, value="" if item.nivel == NIVEL_TIPO else item.codigo)
        cA.font = font_normal
        cA.alignment = align_left

        # Columna B: Nombre (Series en mayúsculas negrita, Subseries negrita, Tipos sangrados)
        from .dataclasses_models import formatear_nombre
        nom_fmt = formatear_nombre(item.nombre, item.nivel)
        nom = ("    " + nom_fmt) if item.nivel == NIVEL_TIPO else nom_fmt

        cB = ws.cell(row=r, column=2, value=nom)
        cB.font = font_bold if item.nivel in (NIVEL_SERIE, NIVEL_SUBSERIE) else font_normal
        cB.alignment = align_left

        # Columna D: Soporte Papel
        cD = ws.cell(row=r, column=4, value="X" if item.soporte_papel else "")
        cD.font = font_normal
        cD.alignment = align_center

        # Columna E: Soporte Electrónico (extensión)
        cE = ws.cell(row=r, column=5, value=(item.extensiones or "X") if item.soporte_electronico else "")
        cE.font = font_normal
        cE.alignment = align_center

        # Columnas F-M: Retención, Disposición, Reproducción, Procedimiento (Series y Subseries)
        if item.nivel != NIVEL_TIPO:
            if item.retencion_gestion:
                ws.cell(row=r, column=6, value=item.retencion_gestion).alignment = align_center
            if item.retencion_central:
                ws.cell(row=r, column=7, value=item.retencion_central).alignment = align_center
            
            if item.disposicion_final == "C":
                ws.cell(row=r, column=8, value="X").alignment = align_center
            elif item.disposicion_final == "S":
                ws.cell(row=r, column=9, value="X").alignment = align_center
            elif item.disposicion_final == "E":
                ws.cell(row=r, column=10, value="X").alignment = align_center

            if item.reproduccion_tecnica:
                ws.cell(row=r, column=11, value="X").alignment = align_center

            if item.procedimiento:
                cL = ws.cell(row=r, column=12, value=item.procedimiento)
                cL.font = font_normal
                cL.alignment = align_left

        # Calcular altura dinámica de la fila para que todo el texto sea 100% visible
        import math
        ancho_chars_proc = 36  # Ancho útil en caracteres de columnas combinadas L y M
        ancho_chars_nom = 33   # Ancho útil en caracteres de columnas combinadas B y C
        
        lineas_proc = 1
        if item.procedimiento and item.nivel != NIVEL_TIPO:
            lineas = 0
            for parrafo in item.procedimiento.split("\n"):
                p_str = parrafo.strip()
                lineas += max(1, math.ceil(len(p_str) / ancho_chars_proc)) if p_str else 1
            lineas_proc = max(1, lineas)
            
        lineas_nom = 1
        if nom:
            lineas = 0
            for parrafo in nom.split("\n"):
                p_str = parrafo.strip()
                lineas += max(1, math.ceil(len(p_str) / ancho_chars_nom)) if p_str else 1
            lineas_nom = max(1, lineas)
            
        # Guardamos los cálculos para ajustar la fila después
        ws.row_dimensions[r].height = max(16.2, lineas_nom * 13.5 + 4.0)
        alturas_nom[r] = ws.row_dimensions[r].height
        if item.nivel in (NIVEL_SERIE, NIVEL_SUBSERIE):
            lineas_proc_dict[r] = lineas_proc

    # --- Postprocesar grupos para fusionar Procedimiento y ajustar alturas ---
    grupos = []
    r_inicio_grupo = 14
    for i in range(1, n_items):
        if lista_items[i].nivel in (NIVEL_SERIE, NIVEL_SUBSERIE):
            grupos.append((r_inicio_grupo, 14 + i - 1))
            r_inicio_grupo = 14 + i
    if n_items > 0:
        grupos.append((r_inicio_grupo, 14 + n_items - 1))

    for r_inicio, r_fin in grupos:
        ws.merge_cells(start_row=r_inicio, start_column=12, end_row=r_fin, end_column=13)
        # Garantizar que la suma de alturas del grupo soporte el texto del procedimiento
        proc_lines = lineas_proc_dict.get(r_inicio, 1)
        altura_necesaria = max(16.2, proc_lines * 13.5 + 4.0)
        
        altura_actual = sum(alturas_nom.get(r, 16.2) for r in range(r_inicio, r_fin + 1))
        
        if altura_actual < altura_necesaria:
            # Distribuir la diferencia en el último elemento del grupo (para empujar hacia abajo)
            diferencia = altura_necesaria - altura_actual
            ws.row_dimensions[r_fin].height = alturas_nom.get(r_fin, 16.2) + diferencia

    # 3. Bloque de Responsables / Firmas (Fila 33 + delta)
    r_firmas = 33 + delta

    # Descombinar y re-combinar para acomodar 3 firmas en lugar de 2
    for r in range(r_firmas, r_firmas + 4):
        for m in list(ws.merged_cells.ranges):
            if m.min_row == r and m.min_col <= 13:
                ws.unmerge_cells(str(m))
    
    from openpyxl.styles import PatternFill
    fill_gris = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")
    
    # Textos y configuracion general de titulos
    titulos = [
        (1, 3, "Responsable del área de gestión documental de la entidad"),
        (4, 10, "Responsable de Área"),
        (11, 13, "Subdirectora Administrativa y financiera")
    ]
    
    # Aplicar estilos y merge a los Títulos
    for c_start, c_end, texto in titulos:
        ws.merge_cells(start_row=r_firmas, start_column=c_start, end_row=r_firmas, end_column=c_end)
        celda = ws.cell(row=r_firmas, column=c_start, value=texto)
        celda.font = font_bold
        celda.alignment = align_left
        # Pintar el fondo gris y poner borde a TODAS las celdas del merge para que se vea el marco completo
        for col in range(c_start, c_end + 1):
            ws.cell(row=r_firmas, column=col).fill = fill_gris
            ws.cell(row=r_firmas, column=col).border = Border(left=thin, right=thin, top=thin, bottom=thin)

    # Nombres, Cargos, Firmas (cajas blancas con bordes)
    etiquetas = ["Nombre:", "Cargo:", "Firma:"]
    for row_offset in (1, 2, 3):
        r_current = r_firmas + row_offset
        
        # Etiqueta en la primera columna de cada bloque
        ws.cell(row=r_current, column=1, value=etiquetas[row_offset - 1]).font = font_normal
        # En el diseño original, la columna de la etiqueta no se mezcla, los valores van en las celdas combinadas de al lado.
        # Pero para igualar el PDF donde "Nombre:" está al lado del valor, ponemos etiqueta en la 1ra celda y mergeamos el resto.
        # Bloque 1: Etiqueta en col 1, merge 2 a 4
        # Bloque 2: Etiqueta en col 5, merge 6 a 7 (Wait, no cabe. Mejor mergeamos todo y ponemos la etiqueta dentro del valor, o ponemos la etiqueta en la 1ra celda)
        # Vamos a poner los bordes perimetrales a los 3 recuadros
        
        for c_start, c_end, _ in titulos:
            ws.merge_cells(start_row=r_current, start_column=c_start + 1, end_row=r_current, end_column=c_end)
            lbl = ws.cell(row=r_current, column=c_start, value=etiquetas[row_offset - 1])
            lbl.font = font_normal
            lbl.alignment = align_left
            ws.cell(row=r_current, column=c_start + 1).alignment = align_left
            for col in range(c_start, c_end + 1):
                # Aplicamos borde inferior suave y bordes laterales rígidos
                left_border = thin if col == c_start else None
                right_border = thin if col == c_end else None
                bottom_border = thin
                # Top border se hereda del bloque de arriba o es thin
                ws.cell(row=r_current, column=col).border = Border(left=left_border, right=right_border, top=thin, bottom=bottom_border)

    ws.cell(row=r_firmas + 1, column=2, value=encabezado.responsable_gestion_documental)
    ws.cell(row=r_firmas + 2, column=2, value=encabezado.cargo_responsable_gestion_documental)
    
    ws.cell(row=r_firmas + 1, column=5, value=encabezado.responsable_area)
    ws.cell(row=r_firmas + 2, column=5, value=encabezado.cargo_responsable_area)
    
    ws.cell(row=r_firmas + 1, column=12, value=encabezado.superior_jerarquico)
    ws.cell(row=r_firmas + 2, column=12, value=encabezado.cargo_superior_jerarquico)

    # 4. Fechas de Aprobación y Versión (Fila 38 + delta)
    # Limpiamos columna 1 por si había texto viejo de la plantilla
    ws.cell(row=r_firmas + 5, column=1, value="")
    ws.cell(row=r_firmas + 6, column=1, value="")

    for r_offset in (5, 6):
        r_f = r_firmas + r_offset
        # Limpiamos posibles combinaciones heredadas en esa zona
        for m in list(ws.merged_cells.ranges):
            if m.min_row == r_f and m.min_col <= 6:
                ws.unmerge_cells(str(m))
                
        ws.merge_cells(start_row=r_f, start_column=1, end_row=r_f, end_column=2)
        
        celda_lbl = ws.cell(row=r_f, column=1)
        celda_lbl.font = font_bold
        celda_lbl.fill = fill_gris
        celda_lbl.border = Border(left=thin, right=thin, top=thin, bottom=thin)
        ws.cell(row=r_f, column=2).border = Border(left=thin, right=thin, top=thin, bottom=thin)

        celda_val = ws.cell(row=r_f, column=3)
        celda_val.alignment = align_center
        celda_val.border = Border(left=thin, right=thin, top=thin, bottom=thin)

    ws.cell(row=r_firmas + 5, column=1, value="Fecha de Aprobación:")
    ws.cell(row=r_firmas + 5, column=3, value=encabezado.fecha_aprobacion or "-")
    ws.cell(row=r_firmas + 6, column=1, value="Versión de Tabla:")
    ws.cell(row=r_firmas + 6, column=3, value=encabezado.fecha_convalidacion or "-")

    flujo = BytesIO()
    wb.save(flujo)
    flujo.seek(0)
    return flujo


def nombre_archivo(encabezado: EncabezadoTRD) -> str:
    """Nombre sugerido para la descarga, sin caracteres inválidos en Windows."""
    oficina = "".join(
        c if c.isalnum() or c in " -_" else "_" for c in encabezado.oficina_productora
    ).strip()
    return f"TRD_{oficina or 'OFICINA'}_{CODIGO_FORMATO}.xlsx"
