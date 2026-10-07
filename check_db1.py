import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

django_script = """
import os, django, json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from trd.models import ItemTRD

for item in ItemTRD.objects.filter(encabezado_id=1):
    if "'" in item.nombre or "'" in item.procedimiento:
        print(f"FOUND QUOTE IN ID {item.id}: {item.nombre}")
"""

sftp = ssh.open_sftp()
sftp.file('/root/nexus-app/check_quotes_db1.py', 'w').write(django_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/check_quotes_db1.py nexus-web:/app/check_quotes_db1.py && docker exec nexus-web python check_quotes_db1.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
