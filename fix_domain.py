import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

script = """
sed -i 's/tdm.nexusflz.tech/trd.nexusflz.tech/g' /root/modulo-tdm/docker-compose.yml
cd /root/modulo-tdm && docker compose up -d --force-recreate
"""

stdin, stdout, stderr = ssh.exec_command(script)
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
