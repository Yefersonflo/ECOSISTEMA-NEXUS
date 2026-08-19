#!/usr/bin/env python
"""Utilidad de linea de comandos de Django para tareas administrativas."""
import os
import sys

def main():
    """Ejecuta tareas administrativas."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. Esta seguro de que esta instalado y "
            "disponible en su variable de entorno PYTHONPATH? Olvido "
            "activar un entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
