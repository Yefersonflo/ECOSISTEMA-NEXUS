import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

django_script = """
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from trd.models import ItemTRD
for i in ItemTRD.objects.all()[:5]:
    print(f"ID: {i.id}, Nivel: '{i.nivel}'")
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/check_niveles.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/check_niveles.py nexus-web:/app/check_niveles.py && docker exec nexus-web python check_niveles.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
