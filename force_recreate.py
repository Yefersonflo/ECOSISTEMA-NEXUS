import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("cd /root/modulo-tdm && docker compose up -d --force-recreate")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
