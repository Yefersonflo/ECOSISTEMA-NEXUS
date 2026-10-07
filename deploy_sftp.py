import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

ssh.exec_command("rm -rf /root/modulo-tdm && mkdir /root/modulo-tdm")

sftp = ssh.open_sftp()
local_dir = r'C:\Users\YEFERSON\Desktop\Desarrollo y Proyectos\MODULO TABLAS DE RETENCION'

for root, dirs, files in os.walk(local_dir):
    if '.git' in root: continue
    
    remote_dir = '/root/modulo-tdm' + root.replace(local_dir, '').replace('\\', '/')
    try:
        sftp.mkdir(remote_dir)
    except:
        pass
        
    for f in files:
        if f.endswith('.py') or f.endswith('.html') or f.endswith('.txt') or f.endswith('.json') or f.endswith('.png') or f.endswith('.xlsx') or f.endswith('.db') or f.endswith('.db.bak') or f.endswith('Procfile'):
            sftp.put(os.path.join(root, f), remote_dir + '/' + f)

docker_compose = '''version: '3.8'
services:
  tdm-web:
    build: .
    container_name: tdm-web
    restart: always
    networks:
      - coolify
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.tdm.rule=Host(	dm.nexusflz.tech)"
      - "traefik.http.routers.tdm.entrypoints=http,https"
      - "traefik.http.routers.tdm.tls=true"
      - "traefik.http.routers.tdm.tls.certresolver=letsencrypt"
      - "traefik.http.services.tdm.loadbalancer.server.port=8000"
networks:
  coolify:
    external: true
'''

dockerfile = '''FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . .
CMD ["gunicorn", "--chdir", "src", "app:app", "-b", "0.0.0.0:8000"]
'''

sftp.file('/root/modulo-tdm/docker-compose.yml', 'w').write(docker_compose)
sftp.file('/root/modulo-tdm/Dockerfile', 'w').write(dockerfile)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("cd /root/modulo-tdm && docker compose up -d --build")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
