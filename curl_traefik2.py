import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("curl -s -H 'Host: tdm.nexusflz.tech' http://localhost | head -n 20")
print(stdout.read().decode())
ssh.close()
