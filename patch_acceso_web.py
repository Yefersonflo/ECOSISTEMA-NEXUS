import os

base_dir = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web'
views_path = os.path.join(base_dir, 'afiliados', 'views.py')

with open(views_path, 'r', encoding='utf8') as f:
    views_code = f.read()

# Reemplazar la asignación del Profile para que incluya acceso_web=True
views_code = views_code.replace(
    "defaults={'rol': 'SUPER'}", 
    "defaults={'rol': 'SUPER', 'acceso_web': True}"
)
views_code = views_code.replace(
    "defaults={'rol': rol}", 
    "defaults={'rol': rol, 'acceso_web': True}"
)

with open(views_path, 'w', encoding='utf8') as f:
    f.write(views_code)
