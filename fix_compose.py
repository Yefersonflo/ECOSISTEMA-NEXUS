import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('179.236.225.125', username='root', password='YefersonFlo96@')

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

sftp = ssh.open_sftp()
sftp.file('/root/modulo-tdm/docker-compose.yml', 'w').write(docker_compose)
sftp.close()

ssh.exec_command("cd /root/modulo-tdm && docker compose up -d")
ssh.close()
