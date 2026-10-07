import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

# check traefik to see if trd is resolving
stdin, stdout, stderr = ssh.exec_command("curl -s -H 'Host: trd.nexusflz.tech' http://localhost | head -n 20")
print(stdout.read().decode())
ssh.close()
