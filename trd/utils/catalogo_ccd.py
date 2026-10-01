"""Modulo de acceso y consulta al Catalogo Oficial del Cuadro de Clasificacion Documental (CCD).

Carga la estructura jerarquica por oficina:
Oficina -> Series -> Subseries -> Retencion, Disposicion Final y Notas.
"""
from __future__ import annotations

import json
import os
from typing import Any, Optional

RUTA_JSON = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "catalogo_ccd.json")

_CATALOGO_CACHE: list[dict[str, Any]] | None = None


def cargar_catalogo() -> list[dict[str, Any]]:
    """Carga el catalogo completo desde el archivo JSON."""
    global _CATALOGO_CACHE
    if _CATALOGO_CACHE is None:
        if os.path.exists(RUTA_JSON):
            with open(RUTA_JSON, "r", encoding="utf-8") as f:
                _CATALOGO_CACHE = json.load(f)
        else:
            _CATALOGO_CACHE = []
    return _CATALOGO_CACHE


def _normalizar(texto: str) -> str:
    """Elimina tildes, signos y normaliza a mayusculas para comparaciones."""
    import unicodedata
    if not texto:
        return ""
    limpio = unicodedata.normalize("NFD", texto)
    limpio = "".join(c for c in limpio if unicodedata.category(c) != "Mn")
    return limpio.strip().upper()


def obtener_datos_oficina(nombre_o_prefijo: str) -> Optional[dict[str, Any]]:
    """Busca y devuelve los datos y series de una oficina por su codigo/prefijo o nombre."""
    import oficinas
    catalogo = cargar_catalogo()
    busqueda = _normalizar(nombre_o_prefijo)
    if not busqueda:
        return None

    # 1. Busqueda prioritaria por prefijo oficial (codigo de la subdireccion)
    prefijo_oficial = oficinas.prefijo_de(nombre_o_prefijo)
    if prefijo_oficial:
        for of in catalogo:
            if of.get("prefijo") == prefijo_oficial:
                return of

    # 2. Busqueda directa si el valor recibido ya es el codigo/prefijo numerico
    if busqueda.isdigit():
        for of in catalogo:
            if of.get("prefijo") == busqueda:
                return of

    # 3. Busqueda por nombre normalizado
    for of in catalogo:
        if _normalizar(of.get("nombre", "")) == busqueda:
            return of

    # 4. Busqueda por clave completa o coincidencia parcial
    for of in catalogo:
        nom_of = _normalizar(of.get("nombre", ""))
        key_of = _normalizar(of.get("key", ""))
        secc_of = _normalizar(of.get("seccion", ""))
        if busqueda in nom_of or nom_of in busqueda or busqueda in key_of or busqueda in secc_of:
            return of

    return None


def obtener_series_oficina(nombre_o_prefijo: str) -> list[dict[str, Any]]:
    """Devuelve la lista de series disponibles para una oficina."""
    of = obtener_datos_oficina(nombre_o_prefijo)
    if of:
        return of.get("series", [])
    return []


def guardar_catalogo(catalogo: list[dict[str, Any]]) -> None:
    """Guarda el catálogo actualizado en el archivo JSON."""
    global _CATALOGO_CACHE
    _CATALOGO_CACHE = catalogo
    os.makedirs(os.path.dirname(RUTA_JSON), exist_ok=True)
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)


def registrar_serie_o_subserie_personalizada(nombre_o_prefijo: str, serie_cod: str, serie_nom: str, sub_cod: str = "", sub_nom: str = "") -> bool:
    """Registra una serie y/o subserie en el catalogo oficial de la oficina para persistirla a futuro."""
    catalogo = cargar_catalogo()
    of = obtener_datos_oficina(nombre_o_prefijo)
    if not of:
        # Si la oficina no existe en el catálogo, la creamos
        import oficinas
        pref = oficinas.prefijo_de(nombre_o_prefijo) or "00"
        of = {
            "key": f"{pref} - {nombre_o_prefijo.upper()}",
            "prefijo": pref,
            "nombre": nombre_o_prefijo.strip().upper(),
            "seccion": f"{pref} {nombre_o_prefijo.strip().upper()}",
            "series": []
        }
        catalogo.append(of)

    series = of.setdefault("series", [])

    # Si no se especificó código de serie, calcular el siguiente número correlativo
    if not serie_cod:
        codigos_num = []
        for s in series:
            c = str(s.get("codigo", "")).strip()
            if c.isdigit():
                codigos_num.append(int(c))
        siguiente = (max(codigos_num) + 1) if codigos_num else 1
        serie_cod = str(siguiente)

    # Limpiar prefijo en el código si viene con él
    pref = of.get("prefijo", "")
    cod_s_limpio = serie_cod
    if pref and cod_s_limpio.startswith(pref + "."):
        cod_s_limpio = cod_s_limpio[len(pref) + 1:]

    # Buscar si la serie ya existe
    serie_existente = None
    for s in series:
        if s.get("codigo") == cod_s_limpio or _normalizar(s.get("nombre", "")) == _normalizar(serie_nom):
            serie_existente = s
            break

    if not serie_existente:
        serie_existente = {
            "codigo": cod_s_limpio,
            "nombre": serie_nom.strip().upper(),
            "subseries": []
        }
        series.append(serie_existente)
    
    # Si viene subserie, registrarla en la serie si no existe
    if sub_cod or sub_nom:
        subseries = serie_existente.setdefault("subseries", [])
        if not sub_cod and sub_nom:
            sub_nums = []
            for sub in subseries:
                c = str(sub.get("codigo", "")).strip()
                if "." in c:
                    c = c.split(".")[-1]
                if c.isdigit():
                    sub_nums.append(int(c))
            sig_sub = (max(sub_nums) + 1) if sub_nums else 1
            sub_cod = f"{serie_existente['codigo']}.{sig_sub}"

        cod_sub_limpio = sub_cod
        if pref and cod_sub_limpio.startswith(pref + "."):
            cod_sub_limpio = cod_sub_limpio[len(pref) + 1:]
        
        sub_existente = None
        for sub in subseries:
            if sub.get("codigo") == cod_sub_limpio or _normalizar(sub.get("nombre", "")) == _normalizar(sub_nom):
                sub_existente = sub
                break
        
        if not sub_existente:
            from models import formatear_titulo
            subseries.append({
                "codigo": cod_sub_limpio,
                "nombre": formatear_titulo(sub_nom),
                "retencion": 0,
                "disposicion": "",
                "reemplazadas": ""
            })

    guardar_catalogo(catalogo)
    return True


def actualizar_serie_en_catalogo(nombre_o_prefijo: str, cod_actual: str, nuevo_cod: str, nuevo_nom: str) -> bool:
    """Modifica el código o nombre de una serie existente en el catálogo CCD de la oficina."""
    catalogo = cargar_catalogo()
    of = obtener_datos_oficina(nombre_o_prefijo)
    if not of:
        return False
    pref = of.get("prefijo", "")
    
    cod_actual_limpio = cod_actual.strip()
    if pref and cod_actual_limpio.startswith(pref + "."):
        cod_actual_limpio = cod_actual_limpio[len(pref) + 1:]
        
    nuevo_cod_limpio = nuevo_cod.strip()
    if pref and nuevo_cod_limpio.startswith(pref + "."):
        nuevo_cod_limpio = nuevo_cod_limpio[len(pref) + 1:]

    series = of.get("series", [])
    for s in series:
        if s.get("codigo") == cod_actual_limpio:
            s["codigo"] = nuevo_cod_limpio
            if nuevo_nom.strip():
                s["nombre"] = nuevo_nom.strip().upper()
            guardar_catalogo(catalogo)
            return True
    return False


def eliminar_serie_de_catalogo(nombre_o_prefijo: str, cod_serie: str) -> bool:
    """Elimina una serie del catálogo CCD de la oficina especificada."""
    catalogo = cargar_catalogo()
    of = obtener_datos_oficina(nombre_o_prefijo)
    if not of:
        return False
    pref = of.get("prefijo", "")
    cod_limpio = cod_serie.strip()
    if pref and cod_limpio.startswith(pref + "."):
        cod_limpio = cod_limpio[len(pref) + 1:]
    
    series = of.get("series", [])
    of["series"] = [s for s in series if s.get("codigo") != cod_limpio]
    guardar_catalogo(catalogo)
    return True


