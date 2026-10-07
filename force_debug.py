import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

# Hardcode DEBUG = True
stdin, stdout, stderr = ssh.exec_command("docker exec nexus-web bash -c \"sed -i 's/DEBUG = .*/DEBUG = True/g' config/settings.py && kill -HUP 1\"")
print(stdout.read().decode())
ssh.close()
