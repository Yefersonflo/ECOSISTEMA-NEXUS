"""Catalogo de oficinas productoras de COMFACASANARE.

Extraido del formato oficial PADO308-PR004-FADO004 v2.0 (50 paginas).
El prefijo es el primer segmento del codigo de toda serie de esa oficina:
por ejemplo, la serie 64.41 pertenece a MECANISMOS DE PROTECCION AL CESANTE.
"""
from __future__ import annotations

# (prefijo, nombre oficial tal como aparece impreso en el formato)
OFICINAS_OFICIALES: tuple[tuple[str, str], ...] = (
    ("10", "DIRECCION"),
    ("11", "JURIDICA"),
    ("12", "CONTROL INTERNO"),
    ("13", "PLANEACION"),
    ("15", "CALIDAD"),
    ("17", "DESARROLLO SOCIAL"),
    ("21", "TALENTO HUMANO"),
    ("22", "COMPRAS"),
    ("23", "TESORERIA"),
    ("24", "CONTABILIDAD"),
    ("25", "CREDITO"),
    ("26", "CARTERA"),
    ("27", "ADMINISTRACION DOCUMENTAL"),
    ("28", "SEGURIDAD Y SALUD EN EL TRABAJO"),
    ("31", "SISTEMAS"),
    ("32", "APORTES Y PAGOS"),
    ("42", "MERCADEO"),
    ("44", "ATENCION AL CLIENTE"),
    ("52", "VIVIENDA"),
    ("55", "DEPORTES"),
    ("58", "RECREACION Y TURISMO"),
    ("61", "GIMNASIO COMFACASANARE"),
    ("62", "POLITECNICO COMFACASANARE"),
    # El formato oficial imprime "BILIOTECA" (sin la segunda B). Se respeta el
    # texto impreso para que la exportacion coincida con el documento vigente.
    ("63", "CULTURA Y BILIOTECA"),
    ("64", "MECANISMOS DE PROTECCION AL CESANTE"),
)

PREFIJO_POR_OFICINA = {nombre: prefijo for prefijo, nombre in OFICINAS_OFICIALES}
OFICINA_POR_PREFIJO = {prefijo: nombre for prefijo, nombre in OFICINAS_OFICIALES}


def prefijo_de(nombre_oficina: str) -> str:
    """Devuelve el prefijo numerico de una oficina, o cadena vacia si no existe."""
    return PREFIJO_POR_OFICINA.get((nombre_oficina or "").strip().upper(), "")


def coincide_prefijo(codigo: str, nombre_oficina: str) -> bool:
    """Indica si un codigo pertenece a la oficina segun su primer segmento.

    Si la oficina no esta en el catalogo oficial no se puede afirmar lo
    contrario, asi que se considera valido.
    """
    esperado = prefijo_de(nombre_oficina)
    if not esperado:
        return True
    return (codigo or "").split(".")[0] == esperado
