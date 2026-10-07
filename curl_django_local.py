import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

# Since nexus-web uses gunicorn on port 8000
stdin, stdout, stderr = ssh.exec_command("docker exec nexus-web curl -s http://localhost:8000/trd/ | grep 'Panel Principal TRD' | head -n 1")
print(stdout.read().decode())
ssh.close()
