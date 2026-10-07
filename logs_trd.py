import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

stdin, stdout, stderr = ssh.exec_command("docker logs --tail 200 nexus-web")
out = stdout.read().decode()
# let's look for exception
for line in out.splitlines():
    if "Error" in line or "Traceback" in line or "Exception" in line or "500" in line:
        print(line)
ssh.close()
