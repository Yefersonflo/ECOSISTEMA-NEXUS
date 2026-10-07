import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

dockerfile = '''FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc pkg-config libcairo2-dev python3-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . .
CMD ["gunicorn", "--chdir", "src", "app:app", "-b", "0.0.0.0:8000"]
'''

sftp = ssh.open_sftp()
sftp.file('/root/modulo-tdm/Dockerfile', 'w').write(dockerfile)
sftp.close()

ssh.exec_command("cd /root/modulo-tdm && docker compose up -d --build")
ssh.close()
