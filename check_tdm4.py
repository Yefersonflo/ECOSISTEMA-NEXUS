import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("docker ps -a | grep tdm-web")
out1 = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command("ps aux | grep 'docker compose up'")
out2 = stdout.read().decode().strip()

print("Docker ps -a:", out1)
print("Processes:", out2)

ssh.close()
