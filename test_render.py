import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

cmds = [
    "docker cp /root/nexus-app/trd/templates/trd/diligenciar.html nexus-web:/app/trd/templates/trd/diligenciar.html",
    # Test render immediately inside the container!
    "docker exec nexus-web python -c \"import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); import django; django.setup(); from django.template.loader import render_to_string; render_to_string('trd/diligenciar.html')\"",
    "docker exec nexus-web kill -HUP 1"
]

for cmd in cmds:
    print(f"Running: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if out: print(out)
    if err: print("ERR:", err)

ssh.close()
