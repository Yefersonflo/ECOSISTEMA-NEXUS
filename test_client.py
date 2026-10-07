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
    response = c.get('/trd/')
    print(f"Status Code: {response.status_code}")
    if response.status_code == 500:
        print("CONTENT:", response.content.decode('utf-8')[:1000])
except Exception as e:
    import traceback
    traceback.print_exc()
'''

stdin, stdout, stderr = ssh.exec_command(f"docker exec nexus-web python -c '{code}'")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
