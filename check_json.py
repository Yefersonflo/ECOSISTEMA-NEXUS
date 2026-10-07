import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

django_script = """
import os, django, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from trd.models import EncabezadoTRD
from trd.utils import catalogo_ccd

encabezado = EncabezadoTRD.objects.get(id=2)
datos_ccd = catalogo_ccd.obtener_datos_oficina(encabezado.oficina_productora)
print(json.dumps(datos_ccd))
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/check_json.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/check_json.py nexus-web:/app/check_json.py && docker exec nexus-web python check_json.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
