import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

code = '''
from django.conf import settings
print("DEBUG is:", settings.DEBUG)
'''

stdin, stdout, stderr = ssh.exec_command(f"docker exec nexus-web python -c \"import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); import django; django.setup(); {code}\"")
print(stdout.read().decode())
ssh.close()
