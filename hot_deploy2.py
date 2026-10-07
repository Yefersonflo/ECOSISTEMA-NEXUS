import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

cmds = [
    "docker exec nexus-web pip install reportlab",
    "docker exec nexus-web python manage.py migrate",
    "docker exec nexus-web kill -HUP 1"
]

for cmd in cmds:
    print(f"Running: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read() # just read it so it finishes
    stderr.read()

ssh.close()
print("Deploy finished successfully!")
