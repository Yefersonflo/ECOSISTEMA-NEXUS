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
response = c.get('/trd/2/')
with open('/app/rendered_trd_2.html', 'w', encoding='utf-8') as f:
    f.write(response.content.decode('utf-8'))
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/render_html.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/render_html.py nexus-web:/app/render_html.py && docker exec nexus-web python render_html.py && docker cp nexus-web:/app/rendered_trd_2.html /root/rendered_trd_2.html")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
