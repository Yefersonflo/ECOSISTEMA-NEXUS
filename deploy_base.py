import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

cmds = [
    "cd /root/nexus-app && git pull",
    "docker cp /root/nexus-app/templates nexus-web:/app/",
    "docker cp /root/nexus-app/trd nexus-web:/app/",
    "docker restart nexus-web"
]

for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    print(stderr.read().decode())

ssh.close()
