import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

b = chr(96)
docker_compose = f'''version: '3.8'
services:
  tdm-web:
    build: .
    container_name: tdm-web
    restart: always
    networks:
      - coolify
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.tdm.rule=Host({b}tdm.nexusflz.tech{b})"
      - "traefik.http.routers.tdm.entrypoints=http,https"
      - "traefik.http.routers.tdm.tls=true"
      - "traefik.http.routers.tdm.tls.certresolver=letsencrypt"
      - "traefik.http.services.tdm.loadbalancer.server.port=8000"
networks:
  coolify:
    external: true
'''

sftp = ssh.open_sftp()
sftp.file('/root/modulo-tdm/docker-compose.yml', 'w').write(docker_compose)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("cd /root/modulo-tdm && docker compose up -d --force-recreate")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
