import os

template_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\trd\templates\trd\editar_trd.html'

with open(template_path, 'r', encoding='utf8') as f:
    code = f.read()

# Añadir x-cloak al formulario que parpadea
code = code.replace(
    """x-show="formularioAbierto"\n          @submit.prevent="enviarFormulario()\"""",
    """x-show="formularioAbierto"\n          x-cloak\n          @submit.prevent="enviarFormulario()\""""
)

with open(template_path, 'w', encoding='utf8') as f:
    f.write(code)

print("x-cloak añadido exitosamente para evitar el parpadeo visual.")
