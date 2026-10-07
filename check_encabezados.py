import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

django_script = """
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from trd.models import EncabezadoTRD
for e in EncabezadoTRD.objects.all():
    print(f"ID: {e.id}, Oficina: {e.oficina_productora}, Estado: {e.estado}, Items: {e.items.count()}")
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/check_enc.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/check_enc.py nexus-web:/app/check_enc.py && docker exec nexus-web python check_enc.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
