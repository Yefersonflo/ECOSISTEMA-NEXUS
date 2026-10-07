import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

sftp = ssh.open_sftp()
sftp.put(r"C:\Users\YEFERSON\Desktop\Desarrollo y Proyectos\MODULO TABLAS DE RETENCION\data\trd_database.db", "/root/trd_database.db")
sftp.put(r"migrate_trd_data.py", "/root/migrate_trd_data.py")
sftp.close()

cmds = [
    "docker cp /root/trd_database.db nexus-web:/app/trd_database.db",
    "docker cp /root/migrate_trd_data.py nexus-web:/app/migrate_trd_data.py",
    "docker exec nexus-web python migrate_trd_data.py"
]

for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    print(stderr.read().decode())

ssh.close()
