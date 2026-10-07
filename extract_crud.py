import os

app_py_path = r"C:\Users\YEFERSON\Desktop\Desarrollo y Proyectos\MODULO TABLAS DE RETENCION\src\app.py"
with open(app_py_path, "r", encoding="utf-8") as f:
    app_py_content = f.read()

# I will create a script that extracts these functions and converts them to Django views
