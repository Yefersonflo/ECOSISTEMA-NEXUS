import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

django_script = """
import os, django, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from trd.models import ItemTRD

for item in ItemTRD.objects.filter(encabezado_id=2, nivel='TIPO'):
    print(f"ID: {item.id}, Nivel: {item.nivel}, Nombre: {item.nombre}, Parent: {item.parent_id}")
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/check_tipos_db.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/check_tipos_db.py nexus-web:/app/check_tipos_db.py && docker exec nexus-web python check_tipos_db.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
