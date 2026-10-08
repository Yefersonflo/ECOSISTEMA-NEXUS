import os
import re

template_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\templates\layout\base.html'

with open(template_path, 'r', encoding='utf8') as f:
    code = f.read()

# 1. Configuración Tailwind y Script inicial seguro (SIN auto-detect, para no dañar a usuarios de día)
tailwind_config_old = "tailwind.config = { theme: { extend: { fontFamily: { 'montserrat': ['Montserrat', 'sans-serif'] }, colors: { comfaBlue: '#1B51A2', comfaRed: '#F05623', comfaYellow: '#FFD101' } } } }"
tailwind_config_new = """tailwind.config = { darkMode: 'class', theme: { extend: { fontFamily: { 'montserrat': ['Montserrat', 'sans-serif'] }, colors: { comfaBlue: '#1B51A2', comfaRed: '#F05623', comfaYellow: '#FFD101' } } } }"""

script_head = """<script>
        // MODO DIA POR DEFECTO. Solo activa oscuro si el usuario lo pide explícitamente.
        if (localStorage.getItem('theme') === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    </script>"""

if tailwind_config_old in code:
    code = code.replace(tailwind_config_old, tailwind_config_new + '\n    ' + script_head)


# 2. CSS de Modo Oscuro "Safe" (No sobreescribe colores corporativos)
dark_css = """
        /* =========================================
           GLOBAL DARK MODE OVERRIDES (SAFE VERSION)
           ========================================= */
        html.dark body { background-color: #0F172A !important; color: #F8FAFC; }
        
        /* Fondos claros a oscuros */
        html.dark .bg-\\[\\#f1f5f9\\], 
        html.dark .bg-slate-50, 
        html.dark .bg-slate-100 { 
            background-color: #0F172A !important; 
        }
        
        /* Tarjetas Blancas a Azul Oscuro */
        html.dark .bg-white, html.dark header { 
            background-color: #1E293B !important; 
            border-color: #334155 !important; 
        }
        
        /* Textos oscuros a claros */
        html.dark .text-slate-900, 
        html.dark .text-slate-800, 
        html.dark .text-slate-700 { color: #F8FAFC !important; }
        html.dark .text-slate-600, 
        html.dark .text-slate-500, 
        html.dark .text-slate-400 { color: #94A3B8 !important; }
        
        /* Bordes */
        html.dark .border-slate-300, 
        html.dark .border-slate-200, 
        html.dark .border-slate-100,
        html.dark .border-slate-50 { border-color: #334155 !important; }

        /* Form elements */
        html.dark input, 
        html.dark select, 
        html.dark textarea {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
            border-color: #334155 !important;
        }
        
        /* Dejar la Sidebar quieta */
        html.dark aside, html.dark aside * {}
"""
if "GLOBAL DARK MODE OVERRIDES" not in code:
    code = code.replace("</style>", dark_css + "\n    </style>")

# 3. Inyectar botón en el header
header_old = """<div class="flex flex-col text-right mr-3 border-r pr-3 border-slate-200">
                    <span class="text-comfaBlue font-black uppercase text-xs tracking-tighter">{{ user.username }}</span>
                    <span class="text-[9px] text-comfaRed uppercase font-black tracking-widest">{{ user.profile.get_rol_display }}</span>
                </div>
                <form action="{% url 'logout' %}" method="post">{% csrf_token %}
                    <button type="submit" class="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-slate-400 hover:text-comfaRed transition-all"><i class="fas fa-power-off"></i></button>
                </form>"""

header_new = """<div class="flex flex-col text-right mr-3 border-r pr-3 border-slate-200">
                    <span class="text-comfaBlue font-black uppercase text-xs tracking-tighter">{{ user.username }}</span>
                    <span class="text-[9px] text-comfaRed uppercase font-black tracking-widest">{{ user.profile.get_rol_display }}</span>
                </div>
                <button onclick="toggleTheme()" id="themeToggleBtn" class="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-slate-400 hover:text-comfaYellow transition-all mr-1 shadow-sm" title="Cambiar Tema">
                    <i class="fas fa-moon"></i>
                </button>
                <form action="{% url 'logout' %}" method="post">{% csrf_token %}
                    <button type="submit" class="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-slate-400 hover:text-comfaRed transition-all shadow-sm"><i class="fas fa-power-off"></i></button>
                </form>"""

if "toggleTheme()" not in code:
    code = code.replace(header_old, header_new)

# 4. Inyectar script de lógica al final del body
theme_script = """
    <script>
        const themeToggleBtn = document.getElementById('themeToggleBtn');
        const themeIcon = themeToggleBtn.querySelector('i');

        function updateThemeIcon() {
            if (document.documentElement.classList.contains('dark')) {
                themeIcon.classList.remove('fa-moon');
                themeIcon.classList.add('fa-sun');
                themeToggleBtn.classList.add('text-comfaYellow');
                themeToggleBtn.classList.remove('text-slate-400');
            } else {
                themeIcon.classList.remove('fa-sun');
                themeIcon.classList.add('fa-moon');
                themeToggleBtn.classList.add('text-slate-400');
                themeToggleBtn.classList.remove('text-comfaYellow');
            }
        }

        function toggleTheme() {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            }
            updateThemeIcon();
        }

        // Init icon
        updateThemeIcon();
    </script>
"""

if "function toggleTheme()" not in code:
    code = code.replace("</body>", theme_script + "\n</body>")

with open(template_path, 'w', encoding='utf8') as f:
    f.write(code)

print("Modo oscuro seguro inyectado exitosamente.")
