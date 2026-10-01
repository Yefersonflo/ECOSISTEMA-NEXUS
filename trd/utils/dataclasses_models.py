"""Modelo de datos del Modulo TRD.

Fiel al formato oficial PADO308-PR004-FADO004 Version 2.0 de COMFACASANARE
(Fecha creacion 02/01/2012 - Fecha ajuste 30/08/2024).

Todas las estructuras son inmutables (dataclasses frozen): para modificar un
registro se produce una copia nueva con `dataclasses.replace`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

# --- Constantes del formato oficial -----------------------------------------

NIVEL_SERIE = "SERIE"
NIVEL_SUBSERIE = "SUBSERIE"
NIVEL_TIPO = "TIPO DOCUMENTAL"
NIVELES = (NIVEL_SERIE, NIVEL_SUBSERIE, NIVEL_TIPO)
PROFUNDIDAD_NIVEL = {NIVEL_SERIE: 0, NIVEL_SUBSERIE: 1, NIVEL_TIPO: 2}

# El formato imprime las columnas de disposicion final como C | S | E.
DISPOSICIONES = {
    "C": "Conservacion Total",
    "S": "Seleccion",
    "E": "Eliminacion",
}
# El instructivo del AGN abrevia la conservacion total como "CT": se acepta como alias.
ALIAS_DISPOSICION = {"CT": "C"}

# Columna "REPRODUCCION TECNICA DEL PAPEL (M/D)".
REPRODUCCIONES = {
    "": "No aplica",
    "D": "Digitalizacion",
}

ENTIDAD_POR_DEFECTO = "Caja de Compensacion Familiar de Casanare - COMFACASANARE"
CODIGO_FORMATO = "PADO308-PR004-FADO004"
VERSION_FORMATO = "2.0"
FECHA_CREACION_FORMATO = "02/01/2012"
FECHA_AJUSTE_FORMATO = "30/08/2024"

PATRON_CODIGO = re.compile(r"^\d+(\.\d+)*$")
RETENCION_MINIMA = 0
RETENCION_MAXIMA = 100


class ValidacionError(ValueError):
    """Se levanta cuando un registro TRD incumple el formato oficial."""


def normalizar_disposicion(valor: str) -> str:
    """Convierte alias como 'CT' a la abreviatura impresa en el formato ('C')."""
    limpio = (valor or "").strip().upper()
    return ALIAS_DISPOSICION.get(limpio, limpio)


def formatear_titulo(texto: str) -> str:
    """Capitaliza la primera letra de cada palabra manteniendo acentos y caracteres especiales."""
    if not texto:
        return ""
    return re.sub(
        r"[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+",
        lambda m: m.group(0)[0].upper() + m.group(0)[1:].lower(),
        texto.strip(),
    )


def formatear_nombre(nombre: str, nivel: str) -> str:
    """Aplica la regla institucional de formato segun el nivel documental:
    - SERIE: MAYUSCULAS SOSTENIDAS
    - SUBSERIE: Tipo Titulo (Primera Letra De Cada Palabra En Mayuscula)
    - TIPO DOCUMENTAL: Tipo Titulo (Primera Letra De Cada Palabra En Mayuscula)
    """
    if not nombre:
        return ""
    if nivel == NIVEL_SERIE:
        return nombre.strip().upper()
    return formatear_titulo(nombre)


# --- Encabezado de la TRD ----------------------------------------------------


@dataclass(frozen=True)
class EncabezadoTRD:
    """Cabecera institucional de una Tabla de Retencion Documental."""

    oficina_productora: str
    entidad_productora: str = ENTIDAD_POR_DEFECTO
    fecha_creacion: str = FECHA_CREACION_FORMATO
    fecha_ajuste: str = FECHA_AJUSTE_FORMATO
    fecha_aprobacion: str = ""
    fecha_convalidacion: str = ""
    responsable_gestion_documental: str = ""
    cargo_responsable_gestion_documental: str = ""
    responsable_area: str = ""
    cargo_responsable_area: str = ""
    superior_jerarquico: str = ""
    cargo_superior_jerarquico: str = ""
    version: str = "1.0"
    estado: str = "VIGENTE"
    vigencia_ano: str = ""
    id: Optional[int] = None

    def errores(self) -> list[str]:
        fallos: list[str] = []
        if not self.entidad_productora.strip():
            fallos.append("La entidad productora es obligatoria.")
        if not self.oficina_productora.strip():
            fallos.append("La oficina productora es obligatoria.")
        if not self.fecha_creacion.strip():
            fallos.append("La fecha de creacion es obligatoria.")
        return fallos

    def validar(self) -> "EncabezadoTRD":
        fallos = self.errores()
        if fallos:
            raise ValidacionError(" ".join(fallos))
        return self


# --- Filas de Series / Subseries / Tipos Documentales ------------------------


@dataclass(frozen=True)
class ItemTRD:
    """Una fila de la TRD: Serie, Subserie o Tipo Documental."""

    codigo: str
    nivel: str
    nombre: str
    soporte_papel: bool = False
    soporte_electronico: bool = False
    extensiones: str = ""
    retencion_gestion: int = 0
    retencion_central: int = 0
    disposicion_final: str = ""
    reproduccion_tecnica: str = ""
    procedimiento: str = ""
    encabezado_id: Optional[int] = None
    parent_id: Optional[int] = None
    orden: int = 0
    id: Optional[int] = None

    @property
    def disposicion_nombre(self) -> str:
        return DISPOSICIONES.get(self.disposicion_final, self.disposicion_final)

    @property
    def reproduccion_nombre(self) -> str:
        return REPRODUCCIONES.get(self.reproduccion_tecnica, self.reproduccion_tecnica)

    @property
    def prefijo_oficina(self) -> str:
        """Primer segmento del codigo: identifica la oficina productora."""
        return self.codigo.split(".")[0] if self.codigo else ""

    @property
    def retencion_total(self) -> int:
        return self.retencion_gestion + self.retencion_central

    def errores(self) -> list[str]:
        return (
            _errores_identidad(self)
            + _errores_soporte(self)
            + _errores_retencion(self)
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nivel": self.nivel,
            "nombre": self.nombre,
            "soporte_papel": self.soporte_papel,
            "soporte_electronico": self.soporte_electronico,
            "extensiones": self.extensiones,
            "retencion_gestion": self.retencion_gestion,
            "retencion_central": self.retencion_central,
            "disposicion_final": self.disposicion_final,
            "reproduccion_tecnica": self.reproduccion_tecnica,
            "procedimiento": self.procedimiento,
            "parent_id": self.parent_id,
            "orden": self.orden,
        }

    def validar(self) -> "ItemTRD":
        fallos = self.errores()
        if fallos:
            raise ValidacionError(" ".join(fallos))
        return self


def _errores_identidad(item: ItemTRD) -> list[str]:
    """Valida codigo, nivel y nombre de la fila."""
    fallos: list[str] = []
    if not PATRON_CODIGO.match(item.codigo.strip()):
        fallos.append(
            f"Codigo invalido '{item.codigo}': use digitos separados por punto (ej. 64.41.3)."
        )
    if item.nivel not in NIVELES:
        fallos.append(f"Nivel invalido '{item.nivel}': use {', '.join(NIVELES)}.")
    if not item.nombre.strip():
        fallos.append("El nombre de la serie/subserie/tipo documental es obligatorio.")
    return fallos


def _errores_soporte(item: ItemTRD) -> list[str]:
    """Valida soportes, extensiones, disposicion final y reproduccion tecnica."""
    fallos: list[str] = []
    if not item.soporte_papel and not item.soporte_electronico:
        fallos.append("Debe marcar al menos un soporte (papel o electronico).")
    if item.soporte_electronico and not item.extensiones.strip():
        fallos.append("Indique las extensiones del soporte electronico (ej. .pdf, .xlsx).")
    if item.disposicion_final and item.disposicion_final not in DISPOSICIONES:
        fallos.append(
            f"Disposicion final invalida '{item.disposicion_final}': use C, S o E."
        )
    if item.reproduccion_tecnica not in REPRODUCCIONES:
        fallos.append(
            f"Reproduccion tecnica invalida '{item.reproduccion_tecnica}': use D o vacio."
        )
    return fallos


def _errores_retencion(item: ItemTRD) -> list[str]:
    """Valida los tiempos de retencion en gestion y central."""
    fallos: list[str] = []
    for etiqueta, valor in (
        ("Archivo de Gestion", item.retencion_gestion),
        ("Archivo Central", item.retencion_central),
    ):
        if isinstance(valor, bool) or not isinstance(valor, int):
            fallos.append(f"La retencion en {etiqueta} debe ser un numero entero.")
        elif valor < RETENCION_MINIMA or valor > RETENCION_MAXIMA:
            fallos.append(
                f"La retencion en {etiqueta} debe estar entre "
                f"{RETENCION_MINIMA} y {RETENCION_MAXIMA} anios."
            )
    return fallos


def advertencias(item: ItemTRD) -> list[str]:
    """Avisos no bloqueantes derivados del instructivo oficial del AGN.

    El instructivo (pagina 50 del formato) exige no dejar el Archivo Central en
    cero para series y subseries, y sustentar en 'Procedimiento' toda decision
    de seleccion o eliminacion.
    """
    avisos: list[str] = []
    if item.nivel in (NIVEL_SERIE, NIVEL_SUBSERIE) and item.retencion_central == 0:
        avisos.append(
            "El instructivo pide no dejar el Archivo Central en cero para series y subseries."
        )
    if item.disposicion_final in ("S", "E") and not item.procedimiento.strip():
        avisos.append(
            "Las disposiciones de Seleccion y Eliminacion deben sustentarse en 'Procedimiento'."
        )
    return avisos


def validar_jerarquia(hijo: ItemTRD, padre: Optional[ItemTRD]) -> list[str]:
    """Verifica que el hijo cuelgue correctamente del padre.

    Reglas archivisticas:
    - SERIE: es raiz, no tiene padre.
    - SUBSERIE: cuelga de una SERIE.
    - TIPO DOCUMENTAL: puede colgar de una SERIE (series simples) o de una SUBSERIE (series compuestas).
    - El codigo del hijo debe extender el codigo de su padre (ej: 11.20 -> 11.20.1 o 11.20.5 -> 11.20.5.1).
    """
    if padre is None:
        if hijo.nivel != NIVEL_SERIE:
            return [f"Un '{hijo.nivel}' no puede existir sin un padre."]
        return []

    fallos: list[str] = []
    if hijo.nivel == NIVEL_SERIE:
        fallos.append("Una 'SERIE' no puede tener un padre.")
    elif hijo.nivel == NIVEL_SUBSERIE:
        if padre.nivel != NIVEL_SERIE:
            fallos.append(
                f"Una 'SUBSERIE' solo puede pertenecer a una 'SERIE', no a '{padre.nivel}'."
            )
    elif hijo.nivel == NIVEL_TIPO:
        if padre.nivel not in (NIVEL_SERIE, NIVEL_SUBSERIE):
            fallos.append(
                f"Un 'TIPO DOCUMENTAL' no puede pertenecer a '{padre.nivel}'."
            )

    if not hijo.codigo.startswith(padre.codigo + "."):
        fallos.append(
            f"El codigo '{hijo.codigo}' debe extender al de su padre '{padre.codigo}'."
        )
    return fallos
