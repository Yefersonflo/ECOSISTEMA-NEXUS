import os

base_dir = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web'
gd_path = os.path.join(base_dir, 'templates', 'afiliados', 'gestion_documental.html')

with open(gd_path, 'r', encoding='utf8') as f:
    gd_content = f.read()

# Fix the broken comment
broken_comment = """<!-- <button type="button" onclick="abrirModalRegistro()" class="bg-comfaBlue text-white font-black px-10 py-5 rounded-2xl shadow-xl hover:bg-comfaRed transition-all uppercase text-[11px] tracking-widest flex items-center cursor-pointer">
                    <i class="fas fa-plus-circle mr-3 text-lg"></i> NUEVO REGISTRO EN {{ cat_activa }}
                </button>"""

if broken_comment in gd_content:
    # Completely remove the button instead of commenting it
    gd_content = gd_content.replace(broken_comment, "")
    with open(gd_path, 'w', encoding='utf8') as f:
        f.write(gd_content)
