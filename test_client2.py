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
    response = c.get("/trd/")
    print("Status Code:", response.status_code)
    if response.status_code == 500:
        print("Error content:")
        try:
            print(response.context["exception"])
        except:
            print(response.content.decode()[:1000])
except Exception as e:
    import traceback
    traceback.print_exc()
'''

sftp = ssh.open_sftp()
with sftp.file('/root/test_django.py', 'w') as f:
    f.write(code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/test_django.py nexus-web:/app/test_django.py && docker exec nexus-web python test_django.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
