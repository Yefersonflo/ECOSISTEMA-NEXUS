# 📘 DOCUMENTO MAESTRO DE CONTINUIDAD — ECOSISTEMA NEXUS
**Fecha de corte:** 20 de Agosto de 2026  
**Proyecto:** Ecosistema Tecnológico de Gestión Documental y Archivo Central — COMFACASANARE  
**Repositorio GitHub:** `https://github.com/Yefersonflo/ECOSISTEMA-NEXUS.git`  
**Despliegue Web Oficial:** `https://ecosistema-nexus-web.onrender.com/`

---

## 🏛️ 1. RESUMEN EJECUTIVO Y ARQUITECTURA

El **Ecosistema NEXUS** es una solución integral de archivo físico y digital que conecta dos plataformas sincronizadas en tiempo real:

1. **Plataforma Web (Django 5 + TailwindCSS + Alpine.js + PostgreSQL en Render):**
   - Panel de control institucional en la nube para administración, consulta, visor de bodega, digitalización de PDFs y generación de reportes gerenciales.
2. **Gestor de Escritorio (Python 3.12 + CustomTkinter + PostgreSQL Cloud-First):**
   - Aplicación para taquilla y puestos de trabajo con búsqueda dual (cédula o nombre), modo taquilla con copia rápida de ubicación, generación de reportes interactivos (Excel / PDF) y sincronización bidireccional inmediata con Render.
3. **Base de Datos Central:**
   - **PostgreSQL en Render:** 2.050 expedientes consolidados y sincronizados al 100%.

---

## 🔒 2. MATRIZ OFICIAL DE LOS 4 ROLES IMPLEMENTADOS

El sistema opera bajo un modelo de control de acceso basado en roles (**RBAC**) de 4 niveles jerárquicos:

```
┌─────────────────────────────────────────────────────────────┐
│ 👑 NIVEL 1 — ADMINISTRADOR TOTAL (SUPER / ADMIN)           │
│    • Control total del sistema y base de datos              │
│    • Sesiones activas en vivo y desconexión remota          │
│    • Historial de Logins (IPs y fallos) y Auditoría Global  │
│    • Eliminación definitiva de registros y archivos PDF     │
├─────────────────────────────────────────────────────────────┤
│ 👔 NIVEL 2 — JEFE DE ARCHIVO (JEFE)                        │
│    • Acceso al Dashboard Gerencial con Alertas (+10 años)   │
│    • Generador Dinámico de Reportes (Excel / PDF)           │
│    • Creación y Edición de expedientes                      │
│    • Digitalización y subida de documentos PDF              │
│    • Bitácora de Trazabilidad de operaciones                │
│    • Sin acceso a desconexión remota ni borrado permanente  │
├─────────────────────────────────────────────────────────────┤
│ 🛠️ NIVEL 3 — AUXILIAR DE REGISTRO Y DIGITALIZACIÓN (AUX)    │
│    • Búsqueda ultrarrápida y atención en ventanilla/taquilla│
│    • Copia rápida de ubicación física (Módulo, Estante...)  │
│    • Creación y edición de datos y ubicaciones de carpetas  │
│    • Subida y adjunto de archivos PDF digitalizados         │
│    • Sin acceso a reportes masivos, auditoría ni borrado    │
├─────────────────────────────────────────────────────────────┤
│ 👁️ NIVEL 4 — USUARIO CONSULTA (CONSULTA / USER)             │
│    • Búsqueda por cédula o nombre en modo solo lectura      │
│    • Visualización de ubicación física y lectura de PDFs    │
│    • Bloqueo total de creación, edición, subida o descarga  │
└─────────────────────────────────────────────────────────────┘
```

### 👥 Usuarios Configurados en el Sistema:
- 👑 **Administradores:** `admin` (Pass: `admin123`), `VivianaL` (Pass: `VivianaL123`)
- 👔 **Jefe de Archivo:** `SandraP` (Pass: `SandraP123`)
- 🛠️ **Auxiliares:** `NicolasB` (Pass: `NicolasB123`), `JairN` (Pass: `JairN123`), `AndresL` (Pass: `AndresL123`)
- 👁️ **Consulta:** `user` (Pass: `user123`)

---

## 🛠️ 3. LO QUE SE IMPLEMENTÓ Y ESTÁ 100% OPERATIVO

### A. Módulo de Reportes Parametrizados (Web y Gestor):
* **Filtros Flexibles:**
  * Estado (`Todos`, `ACTIVO`, `INACTIVO`, `MUERTO`).
  * Rango libre de años de inactividad (`Min` y `Max` ej: de 2 a 4 años).
  * Categoría (`TRABAJADOR` / `PATRONAL`).
  * Módulo físico.
* **En la Web (`/reportes-registros/`):** Interfaz limpia, contador en vivo y descarga de Excel con formato azul Comfacasanare `#004A87`.
* **En el Gestor:** Tabla interactiva (`ttk.Treeview`) con columnas, doble clic sobre cualquier fila para abrir de inmediato su ficha, y botones de **Descargar Excel (.xlsx)** e **Imprimir PDF Horizontal Membretado**.

### B. Gestor de Escritorio Inteligente:
* **Búsqueda Dual:** Acepta tanto cédula numérica como nombres/apellidos parciales. Si hay homónimos, abre una ventana emergente de selección rápida.
* **Modo Taquilla:**
  * Botón `📋 Copiar Ubicación` que copia el texto formateado al portapapeles para ventanilla.
  * Atajo de teclado y botón `🧹 Limpiar (F5)`.
  * Atajo `Enter` en el buscador.
* **Selector de Tema:** Alterna entre `🌙 Modo Oscuro` y `☀️ Modo Claro` con persistencia en `config.json`.
* **Cloud-First Resilience:** Cualquier auxiliar puede instalar el programa mediante `Instalador_Gestor_Nexus_Setup.exe` en cualquier computador; funciona directo contra Render sin requerir archivos Excel en `C:\`.

### C. Centro de Seguridad y Auditoría Nexus Guard (Web):
* **Sesiones Activas:** Monitoreo en tiempo real de usuarios conectados con botón de desconexión remota para el Administrador.
* **Historial de Logins:** Registro de intentos exitosos y fallidos con dirección IP y navegador.
* **Bitácora de Trazabilidad:** Historial de cambios unificado (Web + Gestor) con opción de exportar a Excel.

### D. Sincronización Total de Datos:
* Se consolidaron **2.050 expedientes** en PostgreSQL Render (incluyendo el caso `1118565337`).

---

## 💻 4. CÓMO CONTINUAR TRABAJANDO EN TU PC DE MESA

Cuando vayas a tu computador de escritorio (PC de mesa):

### Paso 1: Clonar el Repositorio de GitHub
Abre una terminal (PowerShell o Git Bash) y ejecuta:
```bash
git clone https://github.com/Yefersonflo/ECOSISTEMA-NEXUS.git
cd ECOSISTEMA-NEXUS
```

### Paso 2: Configurar la Plataforma Web
```bash
cd "4. Plataforma Web"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

### Paso 3: Probar o Modificar el Gestor de Escritorio
```bash
cd "..\3. Gestor de Escritorio"
pip install -r requirements.txt
python gui.py
```

### Paso 4: Recompilar Ejecutable o Instalador (Si haces cambios)
```bash
# Compilar EXE:
pyinstaller --noconfirm --clean Gestor_de_Consultas.spec

# Compilar Instalador Setup con Inno Setup 6:
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "instalador_nexus.iss"
```

---

## 💬 5. PROMPT SUGERIDO PARA EL NUEVO CHAT EN TU PC DE MESA

Copia y pega el siguiente texto en tu nuevo chat en el PC de mesa para retomar el trabajo con máxima precisión:

> *"Hola, estoy continuando el desarrollo del proyecto **ECOSISTEMA NEXUS** (Gestión Documental y Archivo Central de Comfacasanare). Tengo el repositorio clonado de GitHub con la Plataforma Web Django y el Gestor de Escritorio CustomTkinter. Por favor lee el archivo `CONTINUIDAD_PROYECTO_NEXUS.md` en la raíz del proyecto para conocer la arquitectura, los 4 roles (SUPER, JEFE, AUX, USER), los 2.050 registros sincronizados en PostgreSQL Render y lo último que implementamos. Confírmame cuando lo hayas leído para indicarte la siguiente tarea."*

---
*Archivo generado automáticamente por Antigravity AI para continuidad operativa de Comfacasanare.*
