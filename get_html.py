import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

sftp = ssh.open_sftp()
sftp.get('/root/rendered_trd_2.html', 'rendered_trd_2.html')
sftp.close()
ssh.close()
