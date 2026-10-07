import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

django_script = """
import os, django, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from trd.models import ItemTRD

tipos = ItemTRD.objects.filter(nivel__icontains='TIPO')
for t in tipos[:10]:
    print(f"ID: {t.id}, Nivel exacto: '{t.nivel}'")
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/check_nivel_exacto.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/check_nivel_exacto.py nexus-web:/app/check_nivel_exacto.py && docker exec nexus-web python check_nivel_exacto.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
