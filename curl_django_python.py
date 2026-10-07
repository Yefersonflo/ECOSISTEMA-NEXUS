import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

# check using python urllib
script = "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/trd/').getcode())"
stdin, stdout, stderr = ssh.exec_command(f"docker exec nexus-web python -c \"{script}\"")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
