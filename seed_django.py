import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

seed_script = """
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from trd.models import OficinaProductora
from trd.utils.oficinas import OFICINAS_OFICIALES

for prefijo, nombre in OFICINAS_OFICIALES:
    OficinaProductora.objects.get_or_create(prefijo=prefijo, nombre=nombre)
print("Oficinas sembradas exitosamente!")
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/seed_oficinas.py', 'w').write(seed_script)
sftp.close()

cmds = [
    "docker cp /root/nexus-app/seed_oficinas.py nexus-web:/app/seed_oficinas.py",
    "docker exec nexus-web python seed_oficinas.py",
    "docker restart nexus-web"
]

for cmd in cmds:
    print(f"Running: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    print(stderr.read().decode())

ssh.close()
