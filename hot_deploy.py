import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

cmds = [
    "cd /root/nexus-app && git pull",
    "docker cp /root/nexus-app/trd nexus-web:/app/",
    "docker cp /root/nexus-app/config/settings.py nexus-web:/app/config/",
    "docker cp /root/nexus-app/config/urls.py nexus-web:/app/config/",
    "docker cp /root/nexus-app/templates/layout/base.html nexus-web:/app/templates/layout/",
    "docker exec nexus-web pip install reportlab",
    "docker exec nexus-web python manage.py migrate",
    # gunicorn is PID 1 in the container, sending HUP reloads it
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
print("All done!")
