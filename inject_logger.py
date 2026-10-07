import os

path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# I will inject a JS block right before </body> or inside formTRDData to catch Alpine errors
error_logger = """
<script>
window.addEventListener('alpine:init', () => {
    console.log('Alpine is initializing...');
});
window.addEventListener('error', function(e) {
    if (e.message) {
        document.body.insertAdjacentHTML('afterbegin', '<div style="background:red;color:white;padding:10px;z-index:9999;position:fixed;top:0;left:0;right:0;">JS ERROR: ' + e.message + ' at ' + e.filename + ':' + e.lineno + '</div>');
    }
});
</script>
"""

if "window.addEventListener('error'" not in content:
    content = content.replace("</script>\n{% endblock %}", "</script>\n" + error_logger + "{% endblock %}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
