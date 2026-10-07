import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("docker inspect tdm-web | grep traefik.http.routers.tdm.rule")
print(stdout.read().decode())
ssh.close()
