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
Y_CODIGO_FIN, Y_FECHAS_FIN = 549.6, 526.5
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
FIRMAS_ALTOS = (11.0, 13.0, 13.0)             # titulo, Nombre, Cargo
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
    usado_ultima = _alto_pagina_filas(paginas_trd[-1])
    fin_tabla_estimado = Y_CABECERA_FIN - usado_ultima
    y_firmas_fin_estimado = fin_tabla_estimado - FIRMAS_SEPARACION - sum(FIRMAS_ALTOS) - ALTO_FECHAS

    lineas_instructivo, paginas_extra = _planificar_paginas_instructivo(
        y_firmas_fin_estimado, ancho_instructivo
    )
    total_paginas = len(paginas_trd) + paginas_extra

    for numero, pagina in enumerate(paginas_trd, start=1):
        _dibujar_marco(lienzo, encabezado)
        tope = Y_CABECERA_FIN
        fin_tabla = _dibujar_filas(lienzo, pagina, tope=tope) if pagina else tope
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

    _texto(lienzo, X_CELDA_TITULOS + 4.0, 553.8, "CÓDIGO:", NEGRITA, TAM_SUBTITULO)
    _texto(lienzo, X_CELDA_TITULOS + 48.0, 553.8, CODIGO_FORMATO, NORMAL, TAM_SUBTITULO)

    _fecha(lienzo, X_CELDA_TITULOS, X_DIVISOR_FECHAS, "Fecha creación", enc.fecha_creacion)
    _fecha(lienzo, X_DIVISOR_FECHAS, X_DER, "Fecha ajuste", enc.fecha_ajuste)

    centro_derecha = (X_CELDA_TITULOS + X_DER) / 2
    ancho_etiqueta = pdfmetrics.stringWidth("Versión: ", NEGRITA, TAM_SUBTITULO)
    ancho_valor = pdfmetrics.stringWidth(VERSION_FORMATO, NORMAL, TAM_SUBTITULO)
    x = centro_derecha - (ancho_etiqueta + ancho_valor) / 2
    _texto(lienzo, x, 517.8, "Versión:", NEGRITA, TAM_SUBTITULO)
    _texto(lienzo, x + ancho_etiqueta, 517.8, VERSION_FORMATO, NORMAL, TAM_SUBTITULO)


def _fecha(lienzo, x_ini: float, x_fin: float, etiqueta: str, valor: str) -> None:
    """Rotulo en negrita con su fecha debajo, centrados en la subcelda."""
    centro = (x_ini + x_fin) / 2
    _texto_centrado(lienzo, centro, 540.2, etiqueta, NEGRITA, TAM_SUBTITULO)
    _texto_centrado(lienzo, centro, 530.6, valor or "-", NORMAL, TAM_SUBTITULO)


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


class _FilaTabla:
    """Unidad at?mica de paginaci?n: representa un ?tem (Serie, Subserie o Tipo)
    o una l?nea adicional de procedimiento, permitiendo flujo continuo entre p?ginas."""
    __slots__ = ("item", "lineas_nombre", "lineas_proc", "divisor_arriba", "num_lineas")

    def __init__(
        self,
        item: ItemTRD | None,
        lineas_nombre: list[str],
        lineas_proc: list[tuple[str, bool]],
        divisor_arriba: bool = False,
    ):
        self.item = item
        self.lineas_nombre = lineas_nombre
        self.lineas_proc = lineas_proc
        self.divisor_arriba = divisor_arriba
        self.num_lineas = max(len(lineas_nombre), len(lineas_proc), 1)


def _ancho_nombre(item: ItemTRD) -> float:
    """Ancho util del nombre: los tipos documentales van sangrados."""
    return _ancho(1) - (SANGRIA_TIPO if item.nivel == NIVEL_TIPO else 0.0)


def _construir_filas_tabla(items: list[ItemTRD]) -> list[_FilaTabla]:
    """Convierte la lista jer?rquica de ?tems en filas at?micas continuas."""
    grupos: list[tuple[ list[ItemTRD], bool ]] = []
    subseries_en_serie = 0

    for idx, item in enumerate(items):
        if item.nivel == NIVEL_SERIE:
            subseries_en_serie = 0
            grupos.append(([item], idx > 0))
        elif item.nivel == NIVEL_SUBSERIE:
            subseries_en_serie += 1
            divisor = (subseries_en_serie > 1) or (not grupos)
            grupos.append(([item], divisor))
        else:
            if not grupos:
                grupos.append(([item], False))
            else:
                grupos[-1][0].append(item)

    filas: list[_FilaTabla] = []
    for grupo_items, divisor_grupo in grupos:
        lider = grupo_items[0]
        proc_raw = (lider.procedimiento or "") if lider.nivel != NIVEL_TIPO else ""
        lineas_p_str = _ajustar(proc_raw, _ancho(10), TAM_TEXTO) if proc_raw else []
        lineas_p: list[tuple[str, bool]] = [
            (linea, i == len(lineas_p_str) - 1) for i, linea in enumerate(lineas_p_str)
        ]
        cursor_p = 0

        for idx_it, it in enumerate(grupo_items):
            fuente = _fuente(it)
            l_nom = _ajustar(_nombre(it), _ancho_nombre(it), TAM_TEXTO, fuente)
            n_nom = max(len(l_nom), 1)
            slice_p = lineas_p[cursor_p : cursor_p + n_nom]
            cursor_p += n_nom
            filas.append(
                _FilaTabla(
                    item=it,
                    lineas_nombre=l_nom,
                    lineas_proc=slice_p,
                    divisor_arriba=(divisor_grupo if idx_it == 0 else False),
                )
            )

        # Si el procedimiento tiene m?s l?neas que los ?tems del grupo, agregarlas como filas de continuaci?n
        while cursor_p < len(lineas_p):
            filas.append(
                _FilaTabla(
                    item=None,
                    lineas_nombre=[],
                    lineas_proc=[lineas_p[cursor_p]],
                    divisor_arriba=False,
                )
            )
            cursor_p += 1

    return filas


def _alto_pagina_filas(filas_pag: list[_FilaTabla]) -> float:
    """Calcula el alto exacto en puntos que ocupan las filas de una p?gina."""
    if not filas_pag:
        return 0.0
    alto = 2 * RELLENO
    for idx, f in enumerate(filas_pag):
        if idx > 0 and f.divisor_arriba:
            alto += 2 * RELLENO
        alto += f.num_lineas * ALTO_LINEA
    return alto


def _paginar(items: list[ItemTRD]) -> list[list[_FilaTabla]]:
    """Reparte las filas de manera continua p?gina por p?gina hasta agotar el espacio disponible."""
    filas = _construir_filas_tabla(items)
    if not filas:
        return [[]]

    disponible = Y_CABECERA_FIN - Y_PIE
    paginas: list[list[_FilaTabla]] = []
    actual: list[_FilaTabla] = []
    usado = 2 * RELLENO

    for f in filas:
        extra_div = (2 * RELLENO) if (actual and f.divisor_arriba) else 0.0
        alto_f = extra_div + f.num_lineas * ALTO_LINEA

        if actual and (usado + alto_f > disponible):
            paginas.append(actual)
            actual = [f]
            usado = 2 * RELLENO + f.num_lineas * ALTO_LINEA
        else:
            actual.append(f)
            usado += alto_f

    if actual:
        paginas.append(actual)
    return paginas


def _reservar_espacio_de_firmas(
    paginas: list[list[_FilaTabla]],
) -> list[list[_FilaTabla]]:
    """Garantiza que el bloque de firmas quepa debajo de la tabla de la ?ltima p?gina."""
    usado = _alto_pagina_filas(paginas[-1])
    disponible = Y_CABECERA_FIN - Y_PIE
    if usado + ALTO_FIRMAS <= disponible or not paginas[-1]:
        return paginas
    return paginas + [[]]


def _dibujar_filas(lienzo, filas_pag: list[_FilaTabla], tope: float = Y_CABECERA_FIN) -> float:
    """Dibuja las filas continuas de una p?gina y devuelve la coordenada Y del borde inferior."""
    if not filas_pag:
        return tope

    y_cursor = tope - RELLENO
    ancho_proc = _ancho(10)
    x_proc = COLUMNAS_X[10] + RELLENO

    for idx, fila in enumerate(filas_pag):
        if idx > 0 and fila.divisor_arriba:
            y_cursor -= RELLENO
            lienzo.line(X_IZQ, y_cursor, X_DER, y_cursor)
            y_cursor -= RELLENO

        y_primera_linea = y_cursor - TAM_TEXTO
        item = fila.item

        if item is not None:
            fuente = _fuente(item)
            if item.nivel != NIVEL_TIPO:
                _texto(lienzo, COLUMNAS_X[0] + RELLENO, y_primera_linea, item.codigo, NORMAL, TAM_TEXTO)

            sangria = SANGRIA_TIPO if item.nivel == NIVEL_TIPO else 0.0
            for i_nom, linea_nom in enumerate(fila.lineas_nombre):
                _texto(
                    lienzo,
                    COLUMNAS_X[1] + RELLENO + sangria,
                    y_primera_linea - i_nom * ALTO_LINEA,
                    linea_nom,
                    fuente,
                    TAM_TEXTO,
                )

            _centrado(lienzo, 2, y_primera_linea, "X" if item.soporte_papel else "", NORMAL)
            if item.soporte_electronico:
                _texto(lienzo, COLUMNAS_X[3] + RELLENO, y_primera_linea, item.extensiones or "X", NORMAL, TAM_TEXTO)

            if item.nivel != NIVEL_TIPO:
                if item.retencion_gestion:
                    _centrado(lienzo, 4, y_primera_linea, str(item.retencion_gestion), NORMAL)
                if item.retencion_central:
                    _centrado(lienzo, 5, y_primera_linea, str(item.retencion_central), NORMAL)
                for desplazamiento, sigla in enumerate("CSE"):
                    _centrado(
                        lienzo,
                        6 + desplazamiento,
                        y_primera_linea,
                        "X" if item.disposicion_final == sigla else "",
                        NORMAL,
                    )
                if item.reproduccion_tecnica:
                    _centrado(lienzo, 9, y_primera_linea, "X", NORMAL)

        for i_proc, (linea_p, es_ultima_p) in enumerate(fila.lineas_proc):
            _linea_justificada(
                lienzo,
                x_proc,
                y_primera_linea - i_proc * ALTO_LINEA,
                linea_p,
                ancho_proc,
                es_ultima_p,
            )

        y_cursor -= fila.num_lineas * ALTO_LINEA

    y_fin = y_cursor - RELLENO
    lienzo.rect(X_IZQ, y_fin, X_DER - X_IZQ, tope - y_fin)
    for x in COLUMNAS_X[1:-1]:
        lienzo.line(x, y_fin, x, tope)
    return y_fin


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

    t1 = getattr(enc, 'titulo_responsable_1', None) or TITULO_RESPONSABLE
    t2 = getattr(enc, 'titulo_responsable_2', None) or "Responsable de Área"
    t3 = getattr(enc, 'titulo_responsable_3', None) or TITULO_SUPERIOR

    _relleno(lienzo, izquierda, y - alto_titulo, derecha - izquierda, alto_titulo)
    _texto(lienzo, izquierda + 1.3, y - alto_titulo + 3.0, t1,
           NEGRITA, TAM_CABECERA)
    _texto(lienzo, FIRMAS_X[2] + 1.3, y - alto_titulo + 3.0, t2,
           NEGRITA, TAM_CABECERA)
    _texto(lienzo, FIRMAS_X[4] + 1.3, y - alto_titulo + 3.0, t3,
           NEGRITA, TAM_CABECERA)

    renglones = (
        ("Nombre:", enc.responsable_gestion_documental, enc.responsable_area, enc.superior_jerarquico),
        ("Cargo:", enc.cargo_responsable_gestion_documental, enc.cargo_responsable_area, enc.cargo_superior_jerarquico),
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
    ("PARRAFO", "Responsable del área gestión documental de la entidad:", "Se escribirán los nombres y apellidos y cargo del responsable del área gestión documental de la entidad.", 0.0, 4.0),
    ("PARRAFO", "Superior jerarquía:", "Se escribirán los nombres y apellidos y cargo del funcionario(a) administrativo de superior jerarquía.", 0.0, 4.0),
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
    y_tope_nueva = Y_CALIDAD_FIN - 10.0

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
    y_tope_nueva = Y_CALIDAD_FIN - 10.0
    num_pag = pagina_actual

    for l in lineas:
        espacio = l.espacio_previo + l.salto
        if y - espacio < y_minimo:
            _dibujar_pie(lienzo, num_pag, total_paginas)
            lienzo.showPage()
            lienzo.setLineWidth(0.7)
            _bloque_calidad(lienzo, enc)
            _imagen(lienzo, VIGILADO, VIGILADO_CAJA)
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
