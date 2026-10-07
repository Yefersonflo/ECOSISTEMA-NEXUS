import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("docker exec tdm-web curl -s http://localhost:8000/ | head -n 20")
print(stdout.read().decode())
ssh.close()
