import shutil
import os

src = r"C:\Users\YEFERSON\Desktop\Desarrollo y Proyectos\MODULO TABLAS DE RETENCION\src\static"
dst = r"C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\static"

if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)

print("Copied files:")
for root, dirs, files in os.walk(dst):
    for name in files:
        print(os.path.join(root, name))
