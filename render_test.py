import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

code = '''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.template.loader import render_to_string
try:
    render_to_string("trd/diligenciar.html")
    print("Render successful")
except Exception as e:
    import traceback
    traceback.print_exc()
'''

stdin, stdout, stderr = ssh.exec_command(f"docker exec nexus-web python -c '{code}'")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
