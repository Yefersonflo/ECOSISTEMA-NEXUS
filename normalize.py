import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

django_script = """
import os, django, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from trd.models import ItemTRD

# Normalize DB
ItemTRD.objects.filter(nivel__iexact='Tipo').update(nivel='TIPO DOCUMENTAL')
ItemTRD.objects.filter(nivel__iexact='TIPO').update(nivel='TIPO DOCUMENTAL')
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/normalize_tipos.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/normalize_tipos.py nexus-web:/app/normalize_tipos.py && docker exec nexus-web python normalize_tipos.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
