import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("cd /root/nexus-app && ls -la && cat docker-compose.yml 2>/dev/null || echo 'no docker compose'")
print(stdout.read().decode())
ssh.close()
