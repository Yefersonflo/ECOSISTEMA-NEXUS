import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("curl -s -I http://localhost:8000 | grep HTTP")
print("Localhost:8000:", stdout.read().decode().strip())
ssh.close()
