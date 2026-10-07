import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

script = """#!/bin/bash
cd /root
rm -rf modulo-tdm
git clone https://github.com/Yefersonflo/MODULO-TDM.git modulo-tdm
cd modulo-tdm

cat << 'EOF' > Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . .
CMD ["gunicorn", "--chdir", "src", "app:app", "-b", "0.0.0.0:8000"]
EOF

cat << 'EOF' > docker-compose.yml
version: '3.8'
services:
  tdm-web:
    build: .
    container_name: tdm-web
    restart: always
    networks:
      - coolify
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.tdm.rule=Host(\	dm.nexusflz.tech\)"
      - "traefik.http.routers.tdm.entrypoints=http,https"
      - "traefik.http.routers.tdm.tls=true"
      - "traefik.http.routers.tdm.tls.certresolver=letsencrypt"
      - "traefik.http.services.tdm.loadbalancer.server.port=8000"
networks:
  coolify:
    external: true
EOF

docker compose up -d --build
"""

sftp = ssh.open_sftp()
with sftp.file('/root/deploy_tdm.sh', 'w') as f:
    f.write(script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("bash /root/deploy_tdm.sh")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
