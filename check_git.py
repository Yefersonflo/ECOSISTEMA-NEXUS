import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

# Check if we can git pull
stdin, stdout, stderr = ssh.exec_command("cd /root/nexus-app && git remote -v")
print(stdout.read().decode())
ssh.close()
