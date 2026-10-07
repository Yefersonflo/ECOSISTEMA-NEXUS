import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("cd /root/nexus-app && git status && git fetch origin && git reset --hard origin/main")
print(stdout.read().decode())
print(stderr.read().decode())

stdin, stdout, stderr = ssh.exec_command("docker cp /root/nexus-app/trd nexus-web:/app/")
print(stdout.read().decode())

stdin, stdout, stderr = ssh.exec_command("docker restart nexus-web")
print(stdout.read().decode())

ssh.close()
