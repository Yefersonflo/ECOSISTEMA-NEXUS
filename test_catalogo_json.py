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
response = c.get('/trd/catalogo/')
content = response.content.decode('utf-8')
lines = content.split('\\n')
for i, line in enumerate(lines):
    if 'seleccionadas:' in line:
        print("LINE:", line)
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/test_trd_cat.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/test_trd_cat.py nexus-web:/app/test_trd_cat.py && docker exec nexus-web python test_trd_cat.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
