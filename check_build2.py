import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("cd /root/modulo-tdm && docker compose up -d --build")
out = stdout.read()
err = stderr.read()
with open('stdout.txt', 'wb') as f: f.write(out)
with open('stderr.txt', 'wb') as f: f.write(err)
ssh.close()
