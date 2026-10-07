import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

cmds = [
    "docker restart nexus-web"
]

for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()

ssh.close()
