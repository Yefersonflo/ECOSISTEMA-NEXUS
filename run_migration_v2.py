import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

sftp = ssh.open_sftp()
sftp.put(r"migrate_trd_data_v2.py", "/root/migrate_trd_data_v2.py")
sftp.close()

cmds = [
    "docker cp /root/migrate_trd_data_v2.py nexus-web:/app/migrate_trd_data_v2.py",
    "docker exec nexus-web python migrate_trd_data_v2.py"
]

for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    print(stderr.read().decode())

ssh.close()
