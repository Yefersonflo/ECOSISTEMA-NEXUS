import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

# Curl the trd endpoint from the server to bypass auth if possible? 
# Wait, /trd/ requires auth? In urls.py it's just views.diligenciar_trd.
# In views.py, there's NO @login_required! So anyone can access it!
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:8000/trd/ | grep -i 'exception\|traceback\|error\|TemplateSyntaxError' -C 5")
print(stdout.read().decode())
ssh.close()
