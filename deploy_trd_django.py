import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

cmds = [
    "cd /root/nexus-app && git pull",
    "docker cp /root/nexus-app/trd nexus-web:/app/",
    "docker exec nexus-web python manage.py makemigrations trd",
    "docker exec nexus-web python manage.py migrate",
    "docker exec nexus-web kill -HUP 1"
]

for cmd in cmds:
    print(f"Running: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    print(stderr.read().decode())

ssh.close()
