import os

base_dir = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web'
views_path = os.path.join(base_dir, 'afiliados', 'views.py')
template_path = os.path.join(base_dir, 'templates', 'afiliados', 'gestion_usuarios.html')

# 1. Reescribir la vista gestion_usuarios para soportar edición
with open(views_path, 'r', encoding='utf8') as f:
    views_code = f.read()

# Borramos la función anterior y escribimos la nueva
import re
views_code = re.sub(r'@login_required\ndef gestion_usuarios\(request\):.*?(?=@login_required|\Z)', '', views_code, flags=re.DOTALL)

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
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        nombre = request.POST.get('nombre', '')
        apellidos = request.POST.get('apellidos', '')
        password = request.POST.get('password')
        rol = request.POST.get('rol', 'USER')
        is_active = request.POST.get('is_active') == 'on'
        
        if user_id:
            # MODO EDICIÓN
            try:
                user_obj = User.objects.get(id=user_id)
                # Validación para no bloquear al admin principal
                if user_obj.username == 'admin' and not is_active:
                    messages.error(request, 'No puedes desactivar al administrador principal.')
                else:
                    user_obj.username = username
                    user_obj.email = email
                    user_obj.first_name = nombre
                    user_obj.last_name = apellidos
                    user_obj.is_active = is_active
                    
                    if password and password.strip():
                        user_obj.set_password(password)
                        
                    if rol == 'SUPERADMIN':
                        user_obj.is_superuser = True
                        user_obj.is_staff = True
                        user_obj.save()
                        Profile.objects.update_or_create(user=user_obj, defaults={'rol': 'SUPER'})
                    else:
                        if user_obj.username != 'admin':  # Nunca quitar superadmin al usuario root
                            user_obj.is_superuser = False
                            user_obj.is_staff = False
                        user_obj.save()
                        Profile.objects.update_or_create(user=user_obj, defaults={'rol': rol})
                        
                    messages.success(request, f'Usuario {username} actualizado exitosamente.')
            except Exception as e:
                messages.error(request, f'Error al actualizar: {str(e)}')
                
        else:
            # MODO CREACIÓN
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
                    messages.success(request, f'¡El usuario {username} fue creado exitosamente!')
                except Exception as e:
                    messages.error(request, f'Error al crear usuario: {str(e)}')
                    
        return redirect('gestion_usuarios')
        
    return render(request, 'afiliados/gestion_usuarios.html', {'usuarios': usuarios})
"""

with open(views_path, 'a', encoding='utf8') as f:
    f.write(new_view)


# 2. Reescribir el template para añadir botón y modal de edición
template_code = """{% extends 'layout/base.html' %}

{% block title %}Gestión de Personal | Nexus Comfacasanare{% endblock %}

{% block header_title %}Seguridad y Roles{% endblock %}
{% block current_location %}Gestión de Usuarios{% endblock %}

{% block content %}
<div class="space-y-10" x-data="{ 
    showModal: false, 
    showEdit: false, 
    editUser: {} 
}">
    
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
                        <th class="px-8 py-6 text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Acciones</th>
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
                                <i class="fas fa-box-archive {% if u.is_superuser or u.profile.rol == 'JEFE' or u.profile.rol == 'AUX' %}text-comfaBlue{% else %}text-slate-300{% endif %}" title="Puede subir expedientes"></i>
                                <i class="fas fa-sitemap {% if u.is_superuser or u.profile.rol == 'JEFE' %}text-comfaRed{% else %}text-slate-300{% endif %}" title="Puede crear/editar Tablas TRD"></i>
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
                        <td class="px-8 py-6 text-center">
                            <button @click="
                                editUser = {
                                    id: '{{ u.id }}',
                                    username: '{{ u.username }}',
                                    nombre: '{{ u.first_name }}',
                                    apellidos: '{{ u.last_name }}',
                                    email: '{{ u.email }}',
                                    rol: '{% if u.is_superuser %}SUPERADMIN{% else %}{{ u.profile.rol }}{% endif %}',
                                    activo: {% if u.is_active %}true{% else %}false{% endif %}
                                }; 
                                showEdit = true" 
                                class="w-10 h-10 rounded-xl bg-slate-100 text-slate-400 hover:bg-comfaYellow hover:text-white transition-colors flex items-center justify-center cursor-pointer shadow-sm">
                                <i class="fas fa-edit"></i>
                            </button>
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="5" class="text-center py-10 font-bold text-slate-400">No hay usuarios registrados.</td></tr>
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
                            <option value="SUPERADMIN">👑 SUPERADMIN (Control Total)</option>
                            <option value="JEFE">👔 JEFE DE ARCHIVO (Crear Expedientes, TRD completo, Reportes)</option>
                            <option value="AUX">📝 AUXILIAR (Crear Expedientes, TRD Consulta)</option>
                            <option value="USER" selected>👁️ USUARIO DE CONSULTA (Solo Lectura)</option>
                        </select>
                    </div>
                </div>
                
                <button type="submit" class="w-full mt-8 py-5 bg-comfaBlue text-white font-black rounded-2xl shadow-xl hover:bg-comfaRed transition-all uppercase text-[11px] tracking-widest cursor-pointer">
                    Registrar Empleado <i class="fas fa-check-circle ml-2"></i>
                </button>
            </form>
        </div>
    </div>

    <!-- MODAL EDITAR USUARIO -->
    <div x-show="showEdit" class="fixed inset-0 z-50 flex items-center justify-center p-6 bg-comfaBlue/80 backdrop-blur-md" x-cloak>
        <div @click.away="showEdit = false" class="bg-white w-full max-w-2xl rounded-[3rem] shadow-2xl overflow-hidden" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 scale-90" x-transition:enter-end="opacity-100 scale-100">
            <div class="bg-comfaYellow p-8 text-white flex justify-between items-center border-b-8 border-comfaBlue">
                <div>
                    <h3 class="text-xl font-black uppercase tracking-tight">Editar Usuario</h3>
                    <p class="text-[10px] font-bold text-comfaBlue uppercase tracking-widest mt-1">Actualizar Datos y Permisos</p>
                </div>
                <button @click="showEdit = false" type="button" class="text-white/50 hover:text-white transition-colors text-2xl cursor-pointer"><i class="fas fa-times"></i></button>
            </div>
            
            <form method="POST" class="p-10 space-y-6">
                {% csrf_token %}
                <input type="hidden" name="user_id" :value="editUser.id">
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Usuario</label>
                        <input type="text" name="username" :value="editUser.username" required class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaYellow outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Nueva Contraseña <span class="opacity-50">(Opcional)</span></label>
                        <input type="password" name="password" placeholder="Dejar en blanco para no cambiar" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaYellow outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Nombres</label>
                        <input type="text" name="nombre" :value="editUser.nombre" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaYellow outline-none transition-all">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Apellidos</label>
                        <input type="text" name="apellidos" :value="editUser.apellidos" class="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:border-comfaYellow outline-none transition-all">
                    </div>
                    
                    <div class="col-span-2 pt-4">
                        <label class="text-[10px] font-black text-comfaBlue uppercase tracking-widest ml-2 block mb-4"><i class="fas fa-shield-halved mr-2"></i> Cambiar Rol</label>
                        <select name="rol" :value="editUser.rol" class="w-full bg-white border-2 border-slate-200 rounded-xl px-4 py-4 text-sm font-bold text-slate-600 focus:border-comfaYellow outline-none transition-all cursor-pointer shadow-sm">
                            <option value="SUPERADMIN">👑 SUPERADMIN (Control Total)</option>
                            <option value="JEFE">👔 JEFE DE ARCHIVO (Crear Expedientes, TRD completo, Reportes)</option>
                            <option value="AUX">📝 AUXILIAR (Crear Expedientes, TRD Consulta)</option>
                            <option value="USER">👁️ USUARIO DE CONSULTA (Solo Lectura)</option>
                        </select>
                    </div>

                    <div class="col-span-2 mt-4 p-4 bg-slate-50 rounded-2xl border-2 border-slate-100 flex items-center justify-between">
                        <div>
                            <p class="text-xs font-black text-slate-700 uppercase">Estado de la cuenta</p>
                            <p class="text-[9px] font-bold text-slate-400">Si lo desactivas, el usuario no podrá iniciar sesión.</p>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" name="is_active" class="sr-only peer" :checked="editUser.activo">
                            <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                        </label>
                    </div>
                </div>
                
                <button type="submit" class="w-full mt-8 py-5 bg-comfaYellow text-comfaBlue font-black rounded-2xl shadow-xl hover:bg-comfaBlue hover:text-white transition-all uppercase text-[11px] tracking-widest cursor-pointer">
                    Guardar Cambios <i class="fas fa-save ml-2"></i>
                </button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(template_path, 'w', encoding='utf8') as f:
    f.write(template_code)

print("Botón de edición y lógica de backend implementados con éxito.")
