import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

django_script = """
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.test import Client
c = Client(SERVER_NAME='localhost')
response = c.get('/trd/')
content = response.content.decode('utf-8')

if 'COMPRAS' in content:
    print('COMPRAS is in HTML')
if 'JURIDICA' in content:
    print('JURIDICA is in HTML')
if 'No hay tablas' in content:
    print('No hay tablas is in HTML')
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/check_inicio.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/check_inicio.py nexus-web:/app/check_inicio.py && docker exec nexus-web python check_inicio.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
