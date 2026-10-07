import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')
    print("Connected successfully!")
    
    # Let's search for manage.py to find the django project directory
    stdin, stdout, stderr = ssh.exec_command("find / -name manage.py 2>/dev/null")
    paths = stdout.read().decode().strip().split('\n')
    print("Found manage.py paths:")
    for p in paths:
        if p: print(p)
        
    ssh.close()
except Exception as e:
    print("Failed:", e)
