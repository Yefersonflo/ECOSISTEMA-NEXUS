import os

settings_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\config\settings.py'
with open(settings_path, 'r', encoding='utf8') as f:
    code = f.read()

code = code.replace("SESSION_COOKIE_AGE = 1800", "SESSION_COOKIE_AGE = 600")

with open(settings_path, 'w', encoding='utf8') as f:
    f.write(code)

base_path = r'C:\Users\YEFERSON\Desktop\ECOSISTEMA NEXUS\4. Plataforma Web\templates\layout\base.html'
with open(base_path, 'r', encoding='utf8') as f:
    base_code = f.read()

script_inactivity = """
    <script>
        // Redirigir al login después de 10 minutos exactos de inactividad total
        let inactivityTime = function () {
            let time;
            // Reiniciar el contador si hay alguna interacción
            window.onload = resetTimer;
            document.onmousemove = resetTimer;
            document.onkeypress = resetTimer;
            document.onscroll = resetTimer;
            document.onclick = resetTimer;

            function logout() {
                // Alerta suave opcional, o simplemente redirección
                window.location.href = "{% url 'login' %}?next=" + window.location.pathname;
            }

            function resetTimer() {
                clearTimeout(time);
                // 10 minutos = 600,000 milisegundos
                time = setTimeout(logout, 600000);
            }
        };
        // Solo ejecutar si el usuario está autenticado (para no atraparlos en el login)
        {% if user.is_authenticated %}
        inactivityTime();
        {% endif %}
    </script>
</body>"""

if "inactivityTime = function" not in base_code:
    base_code = base_code.replace("</body>", script_inactivity)
    with open(base_path, 'w', encoding='utf8') as f:
        f.write(base_code)

print("Tiempo ajustado a 10 min y redirección inyectada.")
