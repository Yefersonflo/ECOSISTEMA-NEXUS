import os

base_dir = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web'

# 1. Modificar views.py
views_path = os.path.join(base_dir, 'afiliados', 'views.py')
with open(views_path, 'r', encoding='utf8') as f:
    views_code = f.read()

if 'def gestion_usuarios' not in views_code:
    new_view = """

@login_required
def gestion_usuarios(request):
    if not is_super(request.user):
        messages.error(request, 'Solo el Súper Administrador puede gestionar personal.')
        return redirect('gestion_documental')
        
    from django.contrib.auth.models import User
    from .models import Profile
    
    usuarios = User.objects.all().select_related('profile').order_by('-is_superuser', 'username')
    
    if request.method == 'POST':
        # Lógica de crear usuario
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        nombre = request.POST.get('nombre', '')
        apellidos = request.POST.get('apellidos', '')
        password = request.POST.get('password')
        rol = request.POST.get('rol', 'USER')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe en el sistema.')
        else:
            try:
                new_user = User.objects.create_user(username=username, email=email, password=password, first_name=nombre, last_name=apellidos)
                if rol == 'SUPERADMIN':
                    new_user.is_superuser = True
                    new_user.is_staff = True
                    new_user.save()
                    Profile.objects.update_or_create(user=new_user, defaults={'rol': 'SUPER'})
                else:
                    Profile.objects.update_or_create(user=new_user, defaults={'rol': rol})
                
                try:
                    from .models import HistorialAuditoria
                    HistorialAuditoria.objects.create(
                        usuario=request.user,
                        accion='CREAR',
                        modulo='SEGURIDAD',
                        detalles=f'Creación de usuario: {username} con rol {rol}'
                    )
                except: pass
                
                messages.success(request, f'¡El usuario {username} fue creado exitosamente!')
            except Exception as e:
                messages.error(request, f'Error al crear usuario: {str(e)}')
                
        return redirect('gestion_usuarios')
        
    return render(request, 'afiliados/gestion_usuarios.html', {'usuarios': usuarios})
"""
    with open(views_path, 'a', encoding='utf8') as f:
        f.write(new_view)

# 2. Modificar urls.py
urls_path = os.path.join(base_dir, 'config', 'urls.py')
with open(urls_path, 'r', encoding='utf8') as f:
    urls_code = f.read()

if 'gestion_usuarios' not in urls_code:
    urls_code = urls_code.replace("gestion_documental, crear_registro", "gestion_documental, crear_registro, gestion_usuarios")
    urls_code = urls_code.replace(
        "path('nuevo-registro/', crear_registro, name='crear_registro'),",
        "path('nuevo-registro/', crear_registro, name='crear_registro'),\n    path('gestion-personal/', gestion_usuarios, name='gestion_usuarios'),"
    )
    with open(urls_path, 'w', encoding='utf8') as f:
        f.write(urls_code)

# 3. Crear template gestion_usuarios.html
template_path = os.path.join(base_dir, 'templates', 'afiliados', 'gestion_usuarios.html')
template_code = """{% extends 'layout/base.html' %}

{% block title %}Gestión de Personal | Nexus Comfacasanare{% endblock %}

{% block header_title %}Seguridad y Roles{% endblock %}
{% block current_location %}Gestión de Usuarios{% endblock %}

{% block content %}
<div class="space-y-10" x-data="{ showModal: false }">
    
    <!-- HEADER Y BOTON NUEVO USUARIO -->
    <div class="flex flex-col md:flex-row justify-between items-center gap-6 bg-white p-8 rounded-[2.5rem] shadow-sm border border-slate-100">
        <div>
            <h3 class="text-2xl font-black uppercase tracking-tighter text-slate-800">Directorio de Personal</h3>
            <p class="text-xs font-bold text-slate-400 mt-1">Administra quién tiene acceso al sistema y sus permisos.</p>
        </div>
        <button @click="showModal = true" class="bg-comfaBlue text-white font-black px-8 py-4 rounded-2xl shadow-xl hover:bg-comfaRed transition-all uppercase text-xs tracking-widest flex items-center">
            <i class="fas fa-user-plus mr-3 text-lg"></i> Nuevo Usuario
        </button>
    </div>

    <!-- TABLA DE USUARIOS -->
    <div class="bg-white rounded-[2.5rem] shadow-sm overflow-hidden border border-slate-100">
        <div class="overflow-x-auto">
            <table class="w-full text-left">
                <thead class="bg-slate-50 border-b-2 border-slate-100">
                    <tr>
                        <th class="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Usuario / Nombre</th>
                        <th class="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Rol Asignado</th>
                        <th class="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Permisos Clave</th>
                        <th class="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-widest">Estado</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                    {% for u in usuarios %}
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="px-8 py-6">
                            <div class="flex items-center space-x-4">
                                <div class="w-10 h-10 rounded-full bg-slate-200 flex items-center justify-center text-slate-500 font-bold">
                                    <i class="fas fa-user"></i>
                                </div>
                                <div>
                                    <p class="font-black text-slate-700 uppercase text-sm tracking-tighter">{{ u.username }}</p>
                                    <p class="text-[10px] font-bold text-slate-400">{{ u.first_name }} {{ u.last_name }}</p>
                                </div>
                            </div>
                        </td>
                        <td class="px-8 py-6">
                            {% if u.is_superuser %}
                            <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-lg text-[9px] font-black uppercase tracking-widest"><i class="fas fa-crown mr-1"></i> SUPERADMIN</span>
                            {% elif u.profile.rol == 'JEFE' %}
                            <span class="px-3 py-1 bg-comfaBlue/10 text-comfaBlue rounded-lg text-[9px] font-black uppercase tracking-widest"><i class="fas fa-briefcase mr-1"></i> Jefe de Archivo</span>
                            {% elif u.profile.rol == 'AUX' %}
                            <span class="px-3 py-1 bg-comfaYellow/20 text-yellow-700 rounded-lg text-[9px] font-black uppercase tracking-widest"><i class="fas fa-pen-to-square mr-1"></i> Auxiliar</span>
                            {% else %}
                            <span class="px-3 py-1 bg-slate-100 text-slate-500 rounded-lg text-[9px] font-black uppercase tracking-widest"><i class="fas fa-eye mr-1"></i> Usuario Consulta</span>
                            {% endif %}
                        </td>
                        <td class="px-8 py-6">
                            <div class="flex space-x-2 text-lg">
                                <!-- Archivo -->
                                <i class="fas fa-box-archive {% if u.is_superuser or u.profile.rol == 'JEFE' or u.profile.rol == 'AUX' %}text-comfaBlue{% else %}text-slate-300{% endif %}" title="Puede subir expedientes"></i>
                                <!-- TRD -->
                                <i class="fas fa-sitemap {% if u.is_superuser or u.profile.rol == 'JEFE' %}text-comfaRed{% else %}text-slate-300{% endif %}" title="Puede crear/editar Tablas TRD"></i>
                                <!-- Reportes -->
                                <i class="fas fa-file-excel {% if u.is_superuser or u.profile.rol == 'JEFE' %}text-green-500{% else %}text-slate-300{% endif %}" title="Puede descargar Reportes Excel"></i>
                            </div>
                        </td>
                        <td class="px-8 py-6">
                            {% if u.is_active %}
                            <span class="px-3 py-1 bg-green-100 text-green-600 rounded-lg text-[9px] font-black uppercase tracking-widest">Activo</span>
                            {% else %}
                            <span class="px-3 py-1 bg-red-100 text-red-600 rounded-lg text-[9px] font-black uppercase tracking-widest">Inactivo</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="4" class="text-center py-10 font-bold text-slate-400">No hay usuarios registrados.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <!-- MODAL NUEVO USUARIO -->
    <div x-show="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-comfaBlue/80 backdrop-blur-md" x-cloak>
        <div @click.away="showModal = false" class="bg-white w-full max-w-2xl rounded-[3rem] shadow-2xl overflow-hidden" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 scale-90" x-transition:enter-end="opacity-100 scale-100">
            <div class="bg-comfaBlue p-8 text-white flex justify-between items-center border-b-8 border-comfaYellow">
                <div>
                    <h3 class="text-xl font-black uppercase tracking-tight">Crear Nuevo Usuario</h3>
                    <p class="text-[10px] font-bold text-comfaYellow uppercase tracking-widest mt-1">Gestión de Seguridad</p>
                </div>
                <button @click="showModal = false" type="button" class="text-white/50 hover:text-white transition-colors text-2xl cursor-pointer"><i class="fas fa-times"></i></button>
            </div>
            
            <form method="POST" class="p-10 space-y-6">
                {% csrf_token %}
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Nombre de Usuario (Para iniciar sesión)</label>
                        <input type="text" name="username" required class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Contraseña</label>
                        <input type="password" name="password" required class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Nombres</label>
                        <input type="text" name="nombre" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Apellidos</label>
                        <input type="text" name="apellidos" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaBlue outline-none transition-all">
                    </div>
                    
                    <div class="col-span-2 pt-4">
                        <label class="text-[10px] font-black text-comfaBlue uppercase tracking-widest ml-2 block mb-4"><i class="fas fa-shield-halved mr-2"></i> Asignación de Rol y Permisos</label>
                        <select name="rol" class="w-full bg-white border-2 border-slate-200 rounded-xl px-4 py-4 text-sm font-bold text-slate-600 focus:border-comfaBlue outline-none transition-all cursor-pointer shadow-sm">
                            <option value="SUPERADMIN">👑 SUPERADMIN (Control Total - Dashboard, Archivo, TRD, Reportes)</option>
                            <option value="JEFE">👔 JEFE DE ARCHIVO (Crear Expedientes, TRD completo, Reportes)</option>
                            <option value="AUX">📝 AUXILIAR (Crear Expedientes. Solo consulta en TRD. Sin reportes)</option>
                            <option value="USER" selected>👁️ USUARIO DE CONSULTA (Solo ver explorador y catálogo TRD. Nada más)</option>
                        </select>
                    </div>
                </div>
                
                <button type="submit" class="w-full mt-8 py-5 bg-comfaBlue text-white font-black rounded-2xl shadow-xl hover:bg-comfaRed transition-all uppercase text-[11px] tracking-widest cursor-pointer">
                    Registrar Empleado <i class="fas fa-check-circle ml-2"></i>
                </button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(template_path, 'w', encoding='utf8') as f:
    f.write(template_code)

# 4. Modificar base.html (añadir en el sidebar)
base_path = os.path.join(base_dir, 'templates', 'layout', 'base.html')
with open(base_path, 'r', encoding='utf8') as f:
    base_code = f.read()

menu_seguridad = """            {% if user.profile.rol == 'SUPER' or user.is_superuser %}
            <a href="{% url 'gestion_usuarios' %}" class="flex items-center space-x-3 p-3 rounded-xl text-white font-bold hover:bg-white/10 {% if '/gestion-personal/' in request.path %}nav-item-active{% endif %}">
                <i class="fas fa-users-gear w-7 text-center text-lg text-purple-400"></i>
                <span class="sidebar-text text-xs uppercase tracking-widest">Gestión de Personal</span>
            </a>
            {% endif %}"""

if "Gestión de Personal" not in base_code:
    base_code = base_code.replace(
        """<a href="{% url 'historial_auditoria' %}" class="flex items-center space-x-3 p-3 rounded-xl text-white font-bold hover:bg-white/10""",
        f"""{menu_seguridad}\n            <a href="{{% url 'historial_auditoria' %}}" class="flex items-center space-x-3 p-3 rounded-xl text-white font-bold hover:bg-white/10"""
    )
    with open(base_path, 'w', encoding='utf8') as f:
        f.write(base_code)

print("Módulo de Gestión de Usuarios inyectado.")
