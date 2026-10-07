import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')
time.sleep(3) # Wait for it to restart
stdin, stdout, stderr = ssh.exec_command("docker logs tdm-web | tail -n 20")
print(stdout.read().decode())
ssh.close()
