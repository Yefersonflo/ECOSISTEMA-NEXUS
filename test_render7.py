import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

code = '''import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.template.loader import render_to_string
try:
    render_to_string("trd/diligenciar.html")
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
'''

sftp = ssh.open_sftp()
with sftp.file('/root/test_render.py', 'w') as f:
    f.write(code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("docker exec nexus-web python /app/test_render.py || docker cp /root/test_render.py nexus-web:/app/ && docker exec nexus-web python test_render.py")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
