import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

code = '''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.test import Client

try:
    c = Client()
    response = c.get("/", HTTP_HOST="app.nexusflz.tech")
    print("Status Code /:", response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
'''

sftp = ssh.open_sftp()
with sftp.file('/root/test_django.py', 'w') as f:
    f.write(code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker exec nexus-web python test_django.py")
print(stdout.read().decode())
ssh.close()
