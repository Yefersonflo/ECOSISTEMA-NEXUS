# Progreso del Proyecto: archivo_caja

## ðŸ› ï¸ Ficha TÃ©cnica
* **TecnologÃ­a:** Django (Python), SQLite (db.sqlite3), Entorno Virtual (env).
* **Arquitectura:** MVC clÃ¡sica de Django con apps modulares.
* **Componentes Principales:**
  * filiados: LÃ³gica de panel, usuarios Nexus, dependencias y sincronizaciÃ³n.
  * documentos: Modelado y visualizaciÃ³n de Documentos, Correspondencia y PQRSF.
  * ubicacion: Modelado del archivo fÃ­sico (MÃ³dulos, Estantes, Bandejas).

## ðŸ“ˆ Estado Actual del Proyecto
* **Venv Reconstruido:** El entorno virtual se recreÃ³ de forma limpia para solucionar corrupciones de sintaxis previas.
* **Lanzador de Escritorio:** Se configurÃ³ un acceso directo (Archivo Caja) que automatiza el puerto 8000, levanta Django y abre Brave directamente en el Login.
* **Seguridad de SesiÃ³n:** Configurada la expiraciÃ³n de sesiÃ³n al cerrar el navegador.

## ðŸ“ PrÃ³ximas Tareas (To-Do)
- [ ] **Inicializar Base de Datos:** Correr migraciones de Django (python manage.py migrate) ya que db.sqlite3 estÃ¡ actualmente en 0 bytes.
- [ ] **Crear Superusuario:** Crear la primera cuenta administrativa (python manage.py createsuperuser) para probar el login.
- [ ] **Configurar SincronizaciÃ³n IMAP:** Validar que las credenciales de correo en settings.py sean correctas para la bandeja de entrada Ãºnica.
