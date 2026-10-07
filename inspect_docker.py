import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

# Check running container details
stdin, stdout, stderr = ssh.exec_command("docker inspect nexus-web")
print(stdout.read().decode())
ssh.close()
