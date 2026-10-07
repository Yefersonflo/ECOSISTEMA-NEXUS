import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

cmds = [
    "cd /root/nexus-app && git pull",
    "docker cp /root/nexus-app/templates/layout/base.html nexus-web:/app/templates/layout/base.html",
]

for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()

ssh.close()
