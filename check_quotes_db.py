import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

django_script = """
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from trd.models import OficinaProductora
for o in OficinaProductora.objects.all():
    if "'" in o.nombre:
        print("FOUND QUOTE:", o.nombre)
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/check_quotes.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/check_quotes.py nexus-web:/app/check_quotes.py && docker exec nexus-web python check_quotes.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
