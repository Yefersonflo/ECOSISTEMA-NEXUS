"""Replica exacta del formato impreso PADO308-PR004-FADO004 v2.0 en PDF.

Las medidas de este modulo NO son estimaciones: se extrajeron del PDF
institucional `Tabla de Retencion Documental.pdf` leyendo su flujo de
contenido (matrices de texto, trazos de rejilla y colocacion de imagenes).
Por eso el dibujo se hace por coordenadas absolutas sobre un lienzo Carta
horizontal y no con flowables: la meta es que el documento generado calce
sobre el original, cambiando solo los datos diligenciados.
"""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Iterable, Sequence

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as lienzo_pdf

from .dataclasses_models import (
    CODIGO_FORMATO,
    NIVEL_SERIE,
    NIVEL_SUBSERIE,
    NIVEL_TIPO,
    VERSION_FORMATO,
    EncabezadoTRD,
    ItemTRD,
)

PAGINA = landscape(letter)  # 792 x 612 (Carta Horizontal)

# --- Geometría exacta proporcional al formato institucional FADO-004 en Excel ---
# Margen simétrico de 25.5 pt a cada lado (ancho imprimible = 741.0 pt)
X_IZQ, X_DER = 25.5, 766.5
COLUMNAS_X: Sequence[float] = (
    25.5,   # 0: CÓDIGO
    66.6,   # 1: SERIES, SUBSERIES Y TIPOS DOCUMENTALES
    231.7,  # 2: SOPORTE Papel
    269.4,  # 3: SOPORTE Electrónico
    325.6,  # 4: RETENCIÓN Archivo de Gestión
    360.4,  # 5: RETENCIÓN Archivo central
    417.0,  # 6: DISPOSICIÓN FINAL C
    439.0,  # 7: DISPOSICIÓN FINAL S
    461.0,  # 8: DISPOSICIÓN FINAL E
    483.0,  # 9: REPRODUCCIÓN TÉCNICA DEL PAPEL (D)
    543.0,  # 10: PROCEDIMIENTO
    766.5,  # Fin tabla
)
TOTAL_COLUMNAS = len(COLUMNAS_X) - 1

# Subcolumnas de cabecera nivel 2
SUBCOLUMNAS_X: Sequence[float] = (269.4, 360.4, 439.0, 461.0)
X_SUBDIVISION_SOPORTES = (231.7, 483.0)  # Alcance de la línea media de cabecera

Y_TOPE = 562.6           # borde superior del marco
Y_CALIDAD_FIN = 513.5    # fin del bloque de calidad (logo + titulos + codigo)
Y_OFICINA_FIN = 455.6    # fin de la franja oficina productora / convenciones
Y_CABECERA_MEDIO = 432.6 # division entre las dos filas de la cabecera
Y_CABECERA_FIN = 407.8   # fin de la cabecera: aqui empiezan los datos
Y_PIE = 60.7             # borde inferior del marco

X_CELDA_LOGO, X_CELDA_TITULOS = 130.5, 600.5
Y_TITULOS_MEDIO = 530.3  # separa "Sistema de gestion" de "Tabla de retencion"
Y_CODIGO_FIN, Y_FECHAS_FIN = 548.6, 529.6
X_DIVISOR_FECHAS = 683.5
X_DIVISOR_CONVENCIONES = 635.0

LOGO_CAJA = (28.5, 520.0, 98.0, 36.0)          # x, y, ancho, alto
VIGILADO_CAJA = (768.5, 60.7, 20.0, 115.0)

# --- Tipografía Oficial: Tahoma (según formato institucional FADO-004) ---
TAM_TEXTO, TAM_SUBTITULO, TAM_CABECERA = 8.0, 7.2, 6.5

# Gris de los encabezados muestreado del formato institucional: #D9D9D9
GRIS_ENCABEZADO = (217 / 255, 217 / 255, 217 / 255)

# Bloque de convenciones (derecha de la franja de oficina productora)
Y_CONVENCIONES_TOPE, Y_CONVENCIONES_TITULO = 502.9, 491.4
Y_CONVENCIONES_FILAS = (490.7, 482.8, 474.1, 465.5)

# Bloque de firmas (A33:K36 en Excel)
FIRMAS_X = (25.5, 65.5, 231.7, 271.7, 483.0, 523.0, 766.5)  # etiqueta|valor de cada columna
FIRMAS_ALTOS = (11.0, 13.0, 13.0, 14.0)       # titulo, Nombre, Cargo, Firma
FIRMAS_SEPARACION = 12.0                       # aire entre la tabla y el bloque
TITULO_RESPONSABLE = "Responsable del área de gestión documental de la entidad"
TITULO_SUPERIOR = "Subdirectora Administrativa y financiera"

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LOGO = ASSETS / "logo_trd_original.png"
VIGILADO = ASSETS / "vigilado_supersubsidio.png"

_FUENTES_WINDOWS = (
    ("Tahoma", Path("C:/Windows/Fonts/tahoma.ttf")),
    ("Tahoma-Bold", Path("C:/Windows/Fonts/tahomabd.ttf")),
    ("Arial", Path("C:/Windows/Fonts/arial.ttf")),
    ("Arial-Bold", Path("C:/Windows/Fonts/arialbd.ttf")),
)


def _registrar_fuentes() -> tuple[str, str]:
    """Usa Tahoma si el equipo la tiene (idéntico a Excel); si no, Arial o Helvetica."""
    try:
        if Path("C:/Windows/Fonts/tahoma.ttf").exists() and Path("C:/Windows/Fonts/tahomabd.ttf").exists():
            if "Tahoma" not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont("Tahoma", "C:/Windows/Fonts/tahoma.ttf"))
            if "Tahoma-Bold" not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont("Tahoma-Bold", "C:/Windows/Fonts/tahomabd.ttf"))
            return "Tahoma", "Tahoma-Bold"
        for nombre, ruta in _FUENTES_WINDOWS:
            if nombre not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(nombre, str(ruta)))
        return "Arial", "Arial-Bold"
    except Exception:
        return "Helvetica", "Helvetica-Bold"


NORMAL, NEGRITA = _registrar_fuentes()

CONVENCIONES = (("C", "Conservación Total"), ("S", "Selección"), ("E", "Eliminación"))

CABECERA_NIVEL_1 = (
    (0, 1, "CÓDIGO"),
    (1, 2, "SERIES, SUBSERIES Y TIPOS DOCUMENTALES"),
    (2, 4, "SOPORTE O FORMATO"),
    (4, 6, "RETENCIÓN"),
    (6, 9, "DISPOSICIÓN FINAL"),
    (9, 10, "REPRODUCCIÓN TÉCNICA DEL PAPEL (D)"),
    (10, 11, "PROCEDIMIENTO"),
)
CABECERA_NIVEL_2 = (
    (2, "Papel"), (3, "Electrónico (extensión)"),
    (4, "Archivo de Gestión"), (5, "Archivo central"),
    (6, "C"), (7, "S"), (8, "E"),
)
# Columnas que no se subdividen: su rotulo se centra en toda la cabecera.
COLUMNAS_SIN_SUBDIVISION = {0, 1, 9, 10}
ALTO_FECHAS = 32.0


def _renderizar_trd_en_lienzo(lienzo, encabezado: EncabezadoTRD, items: Iterable[ItemTRD]) -> None:
    """Renderiza todas las páginas de una TRD (tabla, firmas, instructivo) sobre el lienzo."""
    items_lista = list(items)
    paginas_trd = _reservar_espacio_de_firmas(_paginar(items_lista))
    ancho_instructivo = X_DER - X_IZQ

    # Estimar posicion inferior de la tabla en la ultima pagina
    usado_ultima = sum(_alto_bloque(b) for b in paginas_trd[-1])
    fin_tabla_estimado = Y_CABECERA_FIN - usado_ultima
    y_firmas_fin_estimado = fin_tabla_estimado - FIRMAS_SEPARACION - sum(FIRMAS_ALTOS) - ALTO_FECHAS

    lineas_instructivo, paginas_extra = _planificar_paginas_instructivo(
        y_firmas_fin_estimado, ancho_instructivo
    )
    total_paginas = len(paginas_trd) + paginas_extra

    for numero, pagina in enumerate(paginas_trd, start=1):
        if numero == 1:
            _dibujar_marco(lienzo, encabezado)
            tope = Y_CABECERA_FIN
        else:
            tope = Y_TOPE
        fin_tabla = _dibujar_filas(lienzo, pagina, tope=tope)
        if numero == len(paginas_trd):
            y_fin_firmas = _dibujar_firmas(lienzo, encabezado, fin_tabla)
            _dibujar_flujo_instructivo(
                lienzo, encabezado, lineas_instructivo, y_fin_firmas, numero, total_paginas
            )
        else:
            _dibujar_pie(lienzo, numero, total_paginas)
            lienzo.showPage()


def generar_pdf(encabezado: EncabezadoTRD, items: Iterable[ItemTRD]) -> BytesIO:
    """Construye el PDF individual de una TRD replicando el formato institucional FADO-004."""
    flujo = BytesIO()
    lienzo = lienzo_pdf.Canvas(flujo, pagesize=PAGINA)
    lienzo.setTitle(f"TRD {encabezado.oficina_productora}")
    lienzo.setAuthor("COMFACASANARE")
    lienzo.setSubject(f"{CODIGO_FORMATO} v{VERSION_FORMATO}")

    _renderizar_trd_en_lienzo(lienzo, encabezado, items)

    lienzo.save()
    flujo.seek(0)
    return flujo


def generar_pdf_consolidado(
    oficinas_data: Sequence[tuple[EncabezadoTRD, Sequence[ItemTRD]]],
    titulo: str = "Tablas de Retención Documental Consolidado",
) -> BytesIO:
    """Construye un único PDF consolidado con todas las TRD seleccionadas."""
    flujo = BytesIO()
    lienzo = lienzo_pdf.Canvas(flujo, pagesize=PAGINA)
    lienzo.setTitle(titulo)
    lienzo.setAuthor("COMFACASANARE")
    lienzo.setSubject(f"{CODIGO_FORMATO} v{VERSION_FORMATO} - Consolidado Institucional")

    for enc, items in oficinas_data:
        _renderizar_trd_en_lienzo(lienzo, enc, items)

    lienzo.save()
    flujo.seek(0)
    return flujo


def nombre_archivo(encabezado: EncabezadoTRD) -> str:
    """Nombre sugerido para la descarga, sin caracteres invalidos en Windows."""
    oficina = "".join(
        c if c.isalnum() or c in " -_" else "_" for c in encabezado.oficina_productora
    ).strip()
    return f"TRD_{oficina or 'OFICINA'}_{CODIGO_FORMATO}.pdf"


def nombre_archivo_consolidado(num_oficinas: int = 0) -> str:
    """Nombre sugerido para el PDF consolidado multioficina."""
    if num_oficinas == 1:
        return f"TRD_Oficina_{CODIGO_FORMATO}.pdf"
    elif num_oficinas > 1:
        return f"TRD_Consolidado_{num_oficinas}_Oficinas_{CODIGO_FORMATO}.pdf"
    return f"TRD_Consolidado_Institucional_{CODIGO_FORMATO}.pdf"


# --- Marco fijo del formato --------------------------------------------------


def _dibujar_marco(lienzo, enc: EncabezadoTRD) -> None:
    """Todo lo que se repite en cada pagina del formato impreso."""
    lienzo.setLineWidth(0.7)
    _bloque_calidad(lienzo, enc)
    _oficina_y_convenciones(lienzo, enc)
    _cabecera_tabla(lienzo)
    _imagen(lienzo, VIGILADO, VIGILADO_CAJA)


def _bloque_calidad(lienzo, enc: EncabezadoTRD) -> None:
    """Logo, titulos del sistema de calidad, codigo, fechas y version."""
    lienzo.rect(X_IZQ, Y_CALIDAD_FIN, X_DER - X_IZQ, Y_TOPE - Y_CALIDAD_FIN)
    for x in (X_CELDA_LOGO, X_CELDA_TITULOS):
        lienzo.line(x, Y_CALIDAD_FIN, x, Y_TOPE)

    _imagen(lienzo, LOGO, LOGO_CAJA)

    lienzo.line(X_CELDA_LOGO, Y_TITULOS_MEDIO, X_CELDA_TITULOS, Y_TITULOS_MEDIO)
    centro = (X_CELDA_LOGO + X_CELDA_TITULOS) / 2
    _texto_centrado(lienzo, centro, 543.7, "SISTEMA DE GESTIÓN DE CALIDAD",
                    NEGRITA, TAM_TEXTO)
    _texto_centrado(lienzo, centro, 519.5, "TABLA DE RETENCIÓN DOCUMENTAL",
                    NORMAL, TAM_SUBTITULO)

    for y in (Y_CODIGO_FIN, Y_FECHAS_FIN):
        lienzo.line(X_CELDA_TITULOS, y, X_DER, y)
    # El divisor solo parte la fila de fechas: la version va centrada completa.
    lienzo.line(X_DIVISOR_FECHAS, Y_FECHAS_FIN, X_DIVISOR_FECHAS, Y_CODIGO_FIN)

    _texto(lienzo, X_CELDA_TITULOS + 4.0, 553.4, "CÓDIGO:", NEGRITA, TAM_SUBTITULO)
    _texto(lienzo, X_CELDA_TITULOS + 48.0, 553.4, CODIGO_FORMATO, NORMAL, TAM_SUBTITULO)

    _fecha(lienzo, X_CELDA_TITULOS, X_DIVISOR_FECHAS, "Fecha creación", enc.fecha_creacion)
    _fecha(lienzo, X_DIVISOR_FECHAS, X_DER, "Fecha ajuste", enc.fecha_ajuste)

    centro_derecha = (X_CELDA_TITULOS + X_DER) / 2
    ancho_etiqueta = pdfmetrics.stringWidth("Versión: ", NEGRITA, TAM_SUBTITULO)
    ancho_valor = pdfmetrics.stringWidth(VERSION_FORMATO, NORMAL, TAM_SUBTITULO)
    x = centro_derecha - (ancho_etiqueta + ancho_valor) / 2
    _texto(lienzo, x, 519.0, "Versión:", NEGRITA, TAM_SUBTITULO)
    _texto(lienzo, x + ancho_etiqueta, 519.0, VERSION_FORMATO, NORMAL, TAM_SUBTITULO)


def _fecha(lienzo, x_ini: float, x_fin: float, etiqueta: str, valor: str) -> None:
    """Rotulo en negrita con su fecha debajo, centrados en la subcelda."""
    centro = (x_ini + x_fin) / 2
    _texto_centrado(lienzo, centro, 543.8, etiqueta, NEGRITA, TAM_TEXTO)
    _texto_centrado(lienzo, centro, 533.5, valor or "-", NORMAL, TAM_TEXTO)


def _oficina_y_convenciones(lienzo, enc: EncabezadoTRD) -> None:
    """Franja sin marco: oficina productora a la izquierda, convenciones a la derecha."""
    _texto(lienzo, X_IZQ + 1.5, 493.2, "OFICINA PRODUCTORA:", NEGRITA, TAM_TEXTO)
    ancho = pdfmetrics.stringWidth("OFICINA PRODUCTORA:   ", NEGRITA, TAM_TEXTO)
    _texto(lienzo, X_IZQ + 1.5 + ancho, 493.2, enc.oficina_productora.upper(), NEGRITA, TAM_TEXTO)

    tope, titulo = Y_CONVENCIONES_TOPE, Y_CONVENCIONES_TITULO
    _relleno(lienzo, X_CELDA_TITULOS, titulo, X_DER - X_CELDA_TITULOS, tope - titulo)
    lienzo.rect(X_CELDA_TITULOS, Y_CONVENCIONES_FILAS[-1],
                X_DER - X_CELDA_TITULOS, tope - Y_CONVENCIONES_FILAS[-1])
    lienzo.line(X_CELDA_TITULOS, titulo, X_DER, titulo)
    _texto_centrado(lienzo, (X_CELDA_TITULOS + X_DER) / 2, 493.2,
                    "CONVENCIONES", NEGRITA, TAM_SUBTITULO)

    for indice, (sigla, nombre) in enumerate(CONVENCIONES):
        arriba, abajo = Y_CONVENCIONES_FILAS[indice], Y_CONVENCIONES_FILAS[indice + 1]
        if indice:
            lienzo.line(X_CELDA_TITULOS, arriba, X_DER, arriba)
        lienzo.line(X_DIVISOR_CONVENCIONES, abajo, X_DIVISOR_CONVENCIONES, arriba)
        base = abajo + 2.0
        _texto_centrado(lienzo, (X_CELDA_TITULOS + X_DIVISOR_CONVENCIONES) / 2, base,
                        sigla, NEGRITA, TAM_TEXTO)
        _texto(lienzo, X_DIVISOR_CONVENCIONES + 3.0, base, nombre, NORMAL, TAM_TEXTO)


def _cabecera_tabla(lienzo) -> None:
    """Cabecera gris de dos niveles, con los rotulos centrados como en el original."""
    alto = Y_OFICINA_FIN - Y_CABECERA_FIN
    _relleno(lienzo, X_IZQ, Y_CABECERA_FIN, X_DER - X_IZQ, alto)
    lienzo.rect(X_IZQ, Y_CABECERA_FIN, X_DER - X_IZQ, alto)

    for x in COLUMNAS_X[1:-1]:
        hasta = Y_CABECERA_MEDIO if x in SUBCOLUMNAS_X else Y_OFICINA_FIN
        lienzo.line(x, Y_CABECERA_FIN, x, hasta)
    lienzo.line(X_SUBDIVISION_SOPORTES[0], Y_CABECERA_MEDIO,
                X_SUBDIVISION_SOPORTES[1], Y_CABECERA_MEDIO)

    for inicio, fin, titulo in CABECERA_NIVEL_1:
        abajo = Y_CABECERA_FIN if inicio in COLUMNAS_SIN_SUBDIVISION else Y_CABECERA_MEDIO
        _rotulo(lienzo, COLUMNAS_X[inicio], COLUMNAS_X[fin], Y_OFICINA_FIN, abajo, titulo)

    for indice, titulo in CABECERA_NIVEL_2:
        _rotulo(lienzo, COLUMNAS_X[indice], COLUMNAS_X[indice + 1],
                Y_CABECERA_MEDIO, Y_CABECERA_FIN, titulo)


def _rotulo(lienzo, x_ini: float, x_fin: float, arriba: float, abajo: float,
            texto: str) -> None:
    """Centra un rotulo de cabecera, horizontal y verticalmente, en su celda."""
    lineas = _ajustar(texto, x_fin - x_ini - 4, TAM_CABECERA)
    salto = TAM_CABECERA + 2.2
    y = (arriba + abajo) / 2 + (len(lineas) - 1) * salto / 2 - TAM_CABECERA / 2 + 0.6
    for linea in lineas:
        _texto_centrado(lienzo, (x_ini + x_fin) / 2, y, linea, NORMAL, TAM_CABECERA)
        y -= salto


# --- Datos diligenciados -----------------------------------------------------

ALTO_LINEA = 11.0
RELLENO = 3.0
SANGRIA_TIPO = 8.0


def _agrupar_por_serie(items: list[ItemTRD]) -> list[list[ItemTRD]]:
    """El formato imprime un recuadro por SERIE con sus subseries y tipos dentro."""
    bloques: list[list[ItemTRD]] = []
    for item in items:
        if item.nivel == NIVEL_SERIE or not bloques:
            bloques.append([item])
        else:
            bloques[-1].append(item)
    return bloques


def _lineas_de_item(item: ItemTRD) -> int:
    del_nombre = len(_ajustar(_nombre(item), _ancho_nombre(item), TAM_TEXTO, _fuente(item)))
    return max(del_nombre, 1)


def _lineas_de_bloque(bloque: list[ItemTRD]) -> int:
    """Cuantas lineas de texto ocupa el recuadro de una serie."""
    total_lineas = 0
    g_nom = 0
    g_proc = 0

    for item in bloque:
        if item.nivel in (NIVEL_SERIE, NIVEL_SUBSERIE):
            total_lineas += max(g_nom, g_proc)
            g_nom = _lineas_de_item(item)
            g_proc = len(_ajustar(item.procedimiento or "", _ancho(10), TAM_TEXTO)) if item.procedimiento else 0
        else:
            g_nom += _lineas_de_item(item)

    total_lineas += max(g_nom, g_proc)
    return total_lineas


def _ancho_nombre(item: ItemTRD) -> float:
    """Ancho util del nombre: los tipos documentales van sangrados."""
    return _ancho(1) - (SANGRIA_TIPO if item.nivel == NIVEL_TIPO else 0.0)


def _alto_bloque(bloque: list[ItemTRD]) -> float:
    return _lineas_de_bloque(bloque) * ALTO_LINEA + 2 * RELLENO


def _paginar(items: list[ItemTRD]) -> list[list[list[ItemTRD]]]:
    """Reparte los recuadros de serie por pagina sin partirlos.
    La pagina 1 lleva cabecera (disponible = Y_CABECERA_FIN - Y_PIE).
    Las paginas 2 en adelante usan la pagina completa (disponible = Y_TOPE - Y_PIE).
    """
    paginas, actual, usado = [], [], 0.0
    for bloque in _agrupar_por_serie(items):
        alto = _alto_bloque(bloque)
        disponible = (Y_CABECERA_FIN - Y_PIE) if not paginas else (Y_TOPE - Y_PIE)
        if actual and usado + alto > disponible:
            paginas.append(actual)
            actual, usado = [], 0.0
            disponible = Y_TOPE - Y_PIE
        actual.append(bloque)
        usado += alto
    paginas.append(actual)
    return paginas


def _reservar_espacio_de_firmas(
    paginas: list[list[list[ItemTRD]]],
) -> list[list[list[ItemTRD]]]:
    """Garantiza que el bloque de firmas quepa debajo de la tabla de la ultima pagina."""
    usado = sum(_alto_bloque(b) for b in paginas[-1])
    disponible = (Y_CABECERA_FIN - Y_PIE) if len(paginas) == 1 else (Y_TOPE - Y_PIE)
    if usado + ALTO_FIRMAS <= disponible or not paginas[-1]:
        return paginas
    return paginas + [[]]


def _dibujar_filas(lienzo, bloques: list[list[ItemTRD]], tope: float = Y_CABECERA_FIN) -> float:
    """Dibuja los recuadros de serie de una pagina y devuelve el borde inferior."""
    y = tope
    for bloque in bloques:
        alto = _alto_bloque(bloque)
        _dibujar_bloque(lienzo, bloque, y, alto)
        y -= alto
        lienzo.line(X_IZQ, y, X_DER, y)

    lienzo.rect(X_IZQ, y, X_DER - X_IZQ, tope - y)
    for x in COLUMNAS_X[1:-1]:
        lienzo.line(x, y, x, tope)
    return y


def _dibujar_bloque(lienzo, bloque: list[ItemTRD], tope: float, alto: float) -> None:
    """Un recuadro de serie: codigos, nombres jerarquicos y datos de cada item."""
    y_start = tope - RELLENO - TAM_TEXTO
    subseries_en_bloque = 0

    g_y_inicio = y_start
    g_nom = 0
    g_proc = 0

    for idx, item in enumerate(bloque):
        if item.nivel in (NIVEL_SERIE, NIVEL_SUBSERIE):
            if idx > 0:
                y_start = g_y_inicio - max(g_nom, g_proc) * ALTO_LINEA
                g_y_inicio = y_start
                g_nom = 0
                g_proc = 0

        if item.nivel == NIVEL_SUBSERIE:
            subseries_en_bloque += 1
            if subseries_en_bloque > 1:
                # El separador de subserie va arriba de este grupo, tomando en cuenta TAM_TEXTO y RELLENO
                y_separador = g_y_inicio + TAM_TEXTO + RELLENO
                lienzo.line(X_IZQ, y_separador, X_DER, y_separador)

        item_lineas = _lineas_de_item(item)
        fuente = _fuente(item)
        
        y_item = g_y_inicio - g_nom * ALTO_LINEA

        # Columna 0: Codigo alineado a la izquierda (los tipos documentales no llevan codigo segun normativa)
        if item.nivel != NIVEL_TIPO:
            _texto(lienzo, COLUMNAS_X[0] + RELLENO, y_item, item.codigo, NORMAL, TAM_TEXTO)

        # Columna 1: Nombre con sangria
        sangria = SANGRIA_TIPO if item.nivel == NIVEL_TIPO else 0.0
        y_nom_dibujo = y_item
        for linea in _ajustar(_nombre(item), _ancho_nombre(item), TAM_TEXTO, fuente):
            _texto(lienzo, COLUMNAS_X[1] + RELLENO + sangria, y_nom_dibujo, linea, fuente, TAM_TEXTO)
            y_nom_dibujo -= ALTO_LINEA

        # Columnas 2-3: Soportes (Aplica para Series, Subseries y Tipos Documentales)
        _centrado(lienzo, 2, y_item, "X" if item.soporte_papel else "", NORMAL)
        if item.soporte_electronico:
            _texto(lienzo, COLUMNAS_X[3] + RELLENO, y_item, item.extensiones or "X", NORMAL, TAM_TEXTO)

        # Columnas 4-10: Retencion, Disposicion, Reproduccion y Procedimiento (Solo Series y Subseries)
        if item.nivel != NIVEL_TIPO:
            if item.retencion_gestion:
                _centrado(lienzo, 4, y_item, str(item.retencion_gestion), NORMAL)
            if item.retencion_central:
                _centrado(lienzo, 5, y_item, str(item.retencion_central), NORMAL)
            for desplazamiento, sigla in enumerate("CSE"):
                _centrado(
                    lienzo,
                    6 + desplazamiento,
                    y_item,
                    "X" if item.disposicion_final == sigla else "",
                    NORMAL,
                )
            if item.reproduccion_tecnica:
                _centrado(lienzo, 9, y_item, "X", NORMAL)

            # Columna 10: Procedimiento
            if item.procedimiento:
                _justificado(lienzo, 10, y_item, item.procedimiento)
                g_proc = len(_ajustar(item.procedimiento, _ancho(10), TAM_TEXTO))

        g_nom += item_lineas



def _fuente(item: ItemTRD) -> str:
    """Series y subseries en negrita; tipos documentales en redonda."""
    return NEGRITA if item.nivel in (NIVEL_SERIE, NIVEL_SUBSERIE) else NORMAL


def _nombre(item: ItemTRD) -> str:
    """Aplica la regla de formato: Series en mayusculas, Subseries y Tipos en tipo titulo."""
    from .dataclasses_models import formatear_nombre
    return formatear_nombre(item.nombre, item.nivel)


# --- Utilidades de dibujo ----------------------------------------------------


def _ancho(columna: int) -> float:
    """Ancho util de una columna, ya descontado el relleno lateral."""
    return COLUMNAS_X[columna + 1] - COLUMNAS_X[columna] - 2 * RELLENO


def _ajustar(texto: str, ancho: float, tam: float, fuente: str = NORMAL) -> list[str]:
    """Parte el texto en lineas que quepan en el ancho dado."""
    if not texto:
        return [""]
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = f"{actual} {palabra}".strip()
        if pdfmetrics.stringWidth(prueba, fuente, tam) <= ancho or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    lineas.append(actual)
    return lineas


def _texto(lienzo, x: float, y: float, texto: str, fuente: str, tam: float) -> None:
    lienzo.setFont(fuente, tam)
    lienzo.drawString(x, y, texto)


def _texto_centrado(lienzo, centro: float, y: float, texto: str,
                    fuente: str, tam: float) -> None:
    lienzo.setFont(fuente, tam)
    lienzo.drawCentredString(centro, y, texto)


def _centrado(lienzo, columna: int, y: float, texto: str, fuente: str) -> None:
    """Valor centrado en su columna (X de soporte, retenciones, C/S/E)."""
    if not texto:
        return
    centro = (COLUMNAS_X[columna] + COLUMNAS_X[columna + 1]) / 2
    _texto_centrado(lienzo, centro, y, texto, fuente, TAM_TEXTO)


def _justificado(lienzo, columna: int, tope: float, texto: str) -> None:
    """Texto justificado a ambos margenes, como el procedimiento del original."""
    ancho = _ancho(columna)
    x = COLUMNAS_X[columna] + RELLENO
    lineas = _ajustar(texto, ancho, TAM_TEXTO)
    y = tope
    for indice, linea in enumerate(lineas):
        ultima = indice == len(lineas) - 1
        _linea_justificada(lienzo, x, y, linea, ancho, ultima)
        y -= ALTO_LINEA


def _linea_justificada(lienzo, x: float, y: float, linea: str, ancho: float,
                       ultima: bool) -> None:
    """Reparte el sobrante entre los espacios; la ultima linea no se estira."""
    palabras = linea.split()
    lienzo.setFont(NORMAL, TAM_TEXTO)
    if ultima or len(palabras) < 2:
        lienzo.drawString(x, y, linea)
        return
    solo_texto = sum(pdfmetrics.stringWidth(p, NORMAL, TAM_TEXTO) for p in palabras)
    hueco = (ancho - solo_texto) / (len(palabras) - 1)
    for palabra in palabras:
        lienzo.drawString(x, y, palabra)
        x += pdfmetrics.stringWidth(palabra, NORMAL, TAM_TEXTO) + hueco


def _relleno(lienzo, x: float, y: float, ancho: float, alto: float) -> None:
    """Fondo gris de los encabezados del formato."""
    lienzo.saveState()
    lienzo.setFillColorRGB(*GRIS_ENCABEZADO)
    lienzo.rect(x, y, ancho, alto, stroke=0, fill=1)
    lienzo.restoreState()


def _imagen(lienzo, ruta: Path, caja: tuple[float, float, float, float]) -> None:
    """Dibuja una imagen del formato; su ausencia no invalida el documento."""
    if not ruta.exists():
        return
    x, y, ancho, alto = caja
    lienzo.drawImage(ImageReader(str(ruta)), x, y, ancho, alto, mask="auto")


def _dibujar_pie(lienzo, numero: int, total: int) -> None:
    """Numeracion discreta fuera del marco."""
    if total > 1:
        _texto(lienzo, X_DER - 40, Y_PIE - 12, f"{numero} de {total}", NORMAL, 6.5)


# --- Bloque de firmas --------------------------------------------------------


ALTO_FECHAS = 22.0
ALTO_FIRMAS = sum(FIRMAS_ALTOS) + FIRMAS_SEPARACION + ALTO_FECHAS


def _dibujar_firmas(lienzo, enc: EncabezadoTRD, tope: float) -> None:
    """Recuadro de responsables con renglones separados de Nombre, Cargo y Firma, y fechas."""
    y = tope - FIRMAS_SEPARACION
    izquierda, derecha = FIRMAS_X[0], FIRMAS_X[6]
    alto_titulo = FIRMAS_ALTOS[0]

    _relleno(lienzo, izquierda, y - alto_titulo, derecha - izquierda, alto_titulo)
    _texto(lienzo, izquierda + 1.3, y - alto_titulo + 3.0, TITULO_RESPONSABLE,
           NEGRITA, TAM_CABECERA)
    _texto(lienzo, FIRMAS_X[2] + 1.3, y - alto_titulo + 3.0, "Responsable de Área",
           NEGRITA, TAM_CABECERA)
    _texto(lienzo, FIRMAS_X[4] + 1.3, y - alto_titulo + 3.0, TITULO_SUPERIOR,
           NEGRITA, TAM_CABECERA)

    renglones = (
        ("Nombre:", enc.responsable_gestion_documental, enc.responsable_area, enc.superior_jerarquico),
        ("Cargo:", enc.cargo_responsable_gestion_documental, enc.cargo_responsable_area, enc.cargo_superior_jerarquico),
        ("Firma", "", "", ""),
    )
    y -= alto_titulo
    lienzo.line(izquierda, y, derecha, y)

    for indice, (etiqueta, val1, val2, val3) in enumerate(renglones):
        alto = FIRMAS_ALTOS[indice + 1]
        base = y - alto + 3.0
        _texto(lienzo, FIRMAS_X[0] + 1.3, base, etiqueta, NORMAL, TAM_CABECERA)
        _texto(lienzo, FIRMAS_X[1] + 1.3, base, val1, NORMAL, TAM_CABECERA)
        _texto(lienzo, FIRMAS_X[2] + 1.3, base, etiqueta, NORMAL, TAM_CABECERA)
        _texto(lienzo, FIRMAS_X[3] + 1.3, base, val2, NORMAL, TAM_CABECERA)
        _texto(lienzo, FIRMAS_X[4] + 1.3, base, etiqueta, NORMAL, TAM_CABECERA)
        _texto(lienzo, FIRMAS_X[5] + 1.3, base, val3, NORMAL, TAM_CABECERA)
        y -= alto
        if indice < len(renglones) - 1:
            lienzo.line(izquierda, y, derecha, y)

    lienzo.rect(izquierda, y, derecha - izquierda, tope - FIRMAS_SEPARACION - y)
    for x in FIRMAS_X[1:6]:
        lienzo.line(x, y, x, tope - FIRMAS_SEPARACION - alto_titulo)
    lienzo.line(FIRMAS_X[2], y, FIRMAS_X[2], tope - FIRMAS_SEPARACION)
    lienzo.line(FIRMAS_X[4], y, FIRMAS_X[4], tope - FIRMAS_SEPARACION)

    # Fechas de Aprobación y Convalidación (según formato oficial FADO-004 de Excel)
    alto_f = 12.0
    w_label = 110.0
    w_valor = 132.8
    y_aprobacion = y - 6.0 - alto_f
    izquierda_fechas = 25.5
    w_label = 110.0
    w_valor = 231.7 - 25.5 - w_label

    # Fila Fecha de Aprobación: Recuadro gris para etiqueta + recuadro blanco para fecha
    _relleno(lienzo, izquierda_fechas, y_aprobacion, w_label, alto_f)
    lienzo.rect(izquierda_fechas, y_aprobacion, w_label, alto_f)
    _texto(lienzo, izquierda_fechas + 3.0, y_aprobacion + 3.0, "Fecha de Aprobación:", NEGRITA, TAM_CABECERA)
    lienzo.rect(izquierda_fechas + w_label, y_aprobacion, w_valor, alto_f)
    _texto_centrado(lienzo, izquierda_fechas + w_label + w_valor / 2, y_aprobacion + 3.0,
                    enc.fecha_aprobacion or "-", NORMAL, TAM_CABECERA)

    # Fila Versión de Tabla: Recuadro gris para etiqueta + recuadro blanco para versión
    y_convalidacion = y_aprobacion - alto_f
    _relleno(lienzo, izquierda_fechas, y_convalidacion, w_label, alto_f)
    lienzo.rect(izquierda_fechas, y_convalidacion, w_label, alto_f)
    _texto(lienzo, izquierda_fechas + 3.0, y_convalidacion + 3.0, "Versión de Tabla:", NEGRITA, TAM_CABECERA)
    lienzo.rect(izquierda_fechas + w_label, y_convalidacion, w_valor, alto_f)
    _texto_centrado(lienzo, izquierda_fechas + w_label + w_valor / 2, y_convalidacion + 3.0,
                    enc.fecha_convalidacion or "-", NORMAL, TAM_CABECERA)

    return y_convalidacion - 8.0


# --- Instructivo Oficial de Diligenciamiento FADO-004 -----------------------

INSTRUCTIVO_CONTENIDO = (
    ("TITULO", "INSTRUCTIVO PARA EL DILIGENCIAMIENTO DEL FORMATO DE TABLA DE RETENCIÓN DOCUMENTAL - TRD", "", 0.0, 14.0),
    ("SECCION", "IDENTIFICACIÓN", "", 0.0, 8.0),
    ("PARRAFO", "Entidad productora:", "escribir el nombre completo o razón social de la entidad productora de la documentación a registrar en las TRD.", 0.0, 4.0),
    ("PARRAFO", "Oficina productora:", "consignar el nombre de la unidad administrativa que produce la serie o subserie documental como resultado del ejercicio de sus funciones.", 0.0, 4.0),
    ("SECCION", "FORMATO:", "", 0.0, 8.0),
    ("PARRAFO", "Código:", "registrar los dígitos con los cuales se identificó la serie o subserie documental. Este debe responder al sistema de clasificación documental establecido en la entidad en el Cuadro de Clasificación Documental.", 0.0, 4.0),
    ("PARRAFO", "Series, subseries y tipos documentales:", "consignar el nombre asignado al conjunto de unidades documentales, resultantes de un mismo órgano o sujeto productor como consecuencia de sus funciones (SERIE). A continuación, escribir el nombre asignado a las unidades documentales que forman parte de una serie y que se identifican de forma separada debido a que los tipos documentales varían de acuerdo con el trámite de cada asunto (Subserie). Por último, registrar cada uno de los tipos documentales que conforman la serie o subserie.", 0.0, 4.0),
    ("PARRAFO", "Soporte o Formato:", "indicar frente a cada tipo documental en que soporte o formato se produce el documento. Marcar con una ‘X’ si la información se produce en físico (papel). Si el documento se produce en medio electrónico, indicar el formato electrónico (extensión) en el que se produce el documento de archivo y se preservará.", 0.0, 4.0),
    ("PARRAFO", "Retención en archivo de gestión:", "diligenciar el tiempo que debe permanecer la serie o subserie en el archivo de gestión, expresado en número de años.", 0.0, 4.0),
    ("PARRAFO", "Retención en archivo de central:", "consignar el tiempo que debe permanecer la serie o subserie en el archivo de central, expresado en número de años. No se deben dejar años en cero o en blanco.", 0.0, 4.0),
    ("PARRAFO", "Disposición final:", "indicar el tipo de disposición final asignado a la serie o subserie documental, marcar con una ‘X’ la abreviatura CT si se trata de conservación total, E si es eliminación o S para el caso de selección.", 0.0, 4.0),
    ("PARRAFO", "Reproducción técnica del papel:", "Indicar si con fines de respaldo de la información y preservación de los soportes originales en papel o en otro soporte físico, se dispuso la reproducción por cualquier medio técnico (digitalización) de la serie o subserie. Marcar la opción con una ‘X’", 0.0, 4.0),
    ("PARRAFO", "Procedimiento:", "registrar información referente al proceso de valoración documental y actividades referentes a la implementación de las Tablas de Retención Documental – TRD, tal como:", 0.0, 4.0),
    ("PARRAFO", "Valor informativo:", "descripción detallada del contenido de la serie, subserie o asunto.", 0.0, 3.0),
    ("PARRAFO", "", "Registrar el sustento de la valoración documental por cada una de las series o subseries documentales; revisar que se desarrollen los criterios definidos en la memoria descriptiva", 0.0, 3.0),
    ("PARRAFO", "", "Para las series, o subseries documentales con disposición final conservación total, referir por qué estas agrupaciones documentales son importantes para la ciencia, la cultura, la historia, entre otros, con relación a su valor estético, testimonial o informativo.", 0.0, 3.0),
    ("PARRAFO", "", "Para las series y subseries documentales con disposición final selección, indicar el volumen o porcentaje de selección y referir los criterios cualitativos que se tendrán en cuenta para dicha selección. Registrar que el volumen o porcentaje seleccionado se conservará en su soporte original y el restante de documentos se eliminará de acuerdo con los procedimientos establecidos.", 0.0, 3.0),
    ("PARRAFO", "", "Para las series o subseries documentales con disposición final eliminación, la decisión de eliminación debe estar ampliamente sustentada en el campo de ‘procedimiento’ de acuerdo con el proceso de valoración documental e indicar el área responsable de realizar el proceso y el método a usar. En caso de que se compile en otra serie, subserie o asunto, indicar en cuál y en qué unidad administrativa se conservará.", 0.0, 3.0),
    ("PARRAFO", "", "Registrar el hecho o documento a partir del cual se empiezan a contar los tiempos de retención documental para las series, o subseries documentales", 0.0, 3.0),
    ("PARRAFO", "", "Para las series y subseries documentales que se marca “Reproducción técnica del papel” indicar en qué momento del Ciclo vital del documento se realizará dicha reproducción.", 0.0, 3.0),
    ("SECCION", "RESPONSABLES:", "", 0.0, 8.0),
    ("PARRAFO", "Responsable del área gestión documental de la entidad:", "Se escribirán los nombres y apellidos, cargo, firma del responsable del área gestión documental de la entidad.", 0.0, 4.0),
    ("PARRAFO", "Superior jerarquía:", "Se escribirán los nombres y apellidos, cargo, firma del funcionario(a) administrativo de superior jerarquía.", 0.0, 4.0),
    ("SECCION", "FECHAS:", "", 0.0, 8.0),
    ("PARRAFO", "Fecha de Aprobación:", "consignar la fecha de aprobación las Tablas de Retención Documental – TRD.", 0.0, 4.0),
    ("PARRAFO", "Versión de Tabla:", "consignar la versión de las Tablas de Retención Documental – TRD. (Si aplica)", 0.0, 4.0),
)


class _LineaInstructivo:
    __slots__ = ("tipo", "negrita", "normal", "sangria", "salto", "espacio_previo")

    def __init__(self, tipo: str, negrita: str, normal: str, sangria: float, salto: float, espacio_previo: float = 0.0):
        self.tipo = tipo
        self.negrita = negrita
        self.normal = normal
        self.sangria = sangria
        self.salto = salto
        self.espacio_previo = espacio_previo


def _construir_lineas_instructivo(ancho_max: float) -> list[_LineaInstructivo]:
    """Convierte el instructivo oficial en lineas ajustadas al ancho disponible."""
    lineas: list[_LineaInstructivo] = []
    tam_p = 7.2
    salto_p = 9.2

    for tipo, et, txt, sangria, espacio_previo in INSTRUCTIVO_CONTENIDO:
        if tipo == "TITULO":
            lineas.append(_LineaInstructivo("TITULO", et, "", sangria, 13.0, espacio_previo))
        elif tipo == "SECCION":
            lineas.append(_LineaInstructivo("SECCION", et, "", sangria, 10.5, espacio_previo))
        else:
            w_et = pdfmetrics.stringWidth(et + " ", NEGRITA, tam_p) if et else 0.0
            palabras = txt.split()
            primer_renglon = True
            linea_palabras: list[str] = []
            limite = ancho_max - sangria - w_et

            for p in palabras:
                w_p = pdfmetrics.stringWidth(p + " ", NORMAL, tam_p)
                w_act = sum(pdfmetrics.stringWidth(w + " ", NORMAL, tam_p) for w in linea_palabras)
                if w_act + w_p <= limite:
                    linea_palabras.append(p)
                else:
                    if primer_renglon:
                        lineas.append(_LineaInstructivo("PARRAFO", et, " ".join(linea_palabras),
                                                        sangria, salto_p, espacio_previo))
                        primer_renglon = False
                        limite = ancho_max - sangria
                    else:
                        lineas.append(_LineaInstructivo("PARRAFO", "", " ".join(linea_palabras),
                                                        sangria, salto_p, 0.0))
                    linea_palabras = [p]

            if linea_palabras or primer_renglon:
                if primer_renglon:
                    lineas.append(_LineaInstructivo("PARRAFO", et, " ".join(linea_palabras),
                                                    sangria, salto_p, espacio_previo))
                else:
                    lineas.append(_LineaInstructivo("PARRAFO", "", " ".join(linea_palabras),
                                                    sangria, salto_p, 0.0))

    return lineas


def _planificar_paginas_instructivo(y_inicio: float, ancho_max: float) -> tuple[list[_LineaInstructivo], int]:
    """Calcula cuantas paginas adicionales se requieren para el instructivo continuo."""
    lineas = _construir_lineas_instructivo(ancho_max)
    y = y_inicio
    paginas_extra = 0
    y_minimo = Y_PIE + 10.0
    y_tope_nueva = Y_TOPE

    for l in lineas:
        espacio = l.espacio_previo + l.salto
        if y - espacio < y_minimo:
            paginas_extra += 1
            y = y_tope_nueva
        y -= espacio

    return lineas, paginas_extra


def _dibujar_flujo_instructivo(
    lienzo,
    enc: EncabezadoTRD,
    lineas: list[_LineaInstructivo],
    y_inicio: float,
    pagina_actual: int,
    total_paginas: int,
) -> None:
    """Dibuja el instructivo en flujo continuo full-width sobre la tabla o en paginas nuevas."""
    y = y_inicio
    y_minimo = Y_PIE + 10.0
    y_tope_nueva = Y_TOPE
    num_pag = pagina_actual

    for l in lineas:
        espacio = l.espacio_previo + l.salto
        if y - espacio < y_minimo:
            _dibujar_pie(lienzo, num_pag, total_paginas)
            lienzo.showPage()
            num_pag += 1
            y = y_tope_nueva

        y -= l.espacio_previo

        if l.tipo == "TITULO":
            _texto_centrado(lienzo, (X_IZQ + X_DER) / 2, y, l.negrita, NEGRITA, 9.0)
        elif l.tipo == "SECCION":
            _texto(lienzo, X_IZQ, y, l.negrita, NEGRITA, 8.0)
        else:
            x_act = X_IZQ + l.sangria
            if l.negrita:
                _texto(lienzo, x_act, y, l.negrita, NEGRITA, 7.2)
                x_act += pdfmetrics.stringWidth(l.negrita + " ", NEGRITA, 7.2)
            if l.normal:
                _texto(lienzo, x_act, y, l.normal, NORMAL, 7.2)

        y -= l.salto

    _dibujar_pie(lienzo, num_pag, total_paginas)
    lienzo.showPage()
