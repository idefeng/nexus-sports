# 多域名部署指南 (Ubuntu + Docker + Nginx)

针对您已有一台运行 Docker 的 Ubuntu 服务器且需要部署多个域名的场景，本指南详细说明如何通过 **Nginx 反向代理** 实现 `sports.everyservice.online` 的部署。

## 场景现状与端口规划
- **已有域名**: `https://jpgo.everyservice.online/`
    - 主机端口 `3000` 已被 `app-jpgo-backend-1` 占用。
- **新域名**: `https://sports.everyservice.online/`
- **端口分配建议**:
    - 前端容器: 主机 `8080` -> 容器 `80`
    - 后端容器: 主机 `8000` -> 容器 `8000`
    - *这两个端口与您现有的 3000 端口没有冲突，可以放心使用。*


### 2.1 修改 `docker-compose.yml` (可选)
如果您的 8080 或 8000 端口已被其他程序占用，请修改 `docker-compose.yml` 中的 `ports` 映射：
```yaml
  backend:
    ports:
      - "8001:8000" # 将主机 8001 映射到容器 8000
  frontend:
    ports:
      - "8081:80"   # 将主机 8081 映射到容器 80
```
*注：以下配置均假设您使用默认的 8080 (前端) 和 8000 (后端)。*

---

## 2. Nginx 反向代理配置 (主机端)

在 Ubuntu 主机上安装并配置 Nginx 作为入口：

### 2.1 安装 Nginx
```bash
sudo apt update
sudo apt install nginx
```

### 2.2 创建站点配置
参考您已有的 `jpgo` 配置，请创建文件 `/etc/nginx/sites-available/nexus-sports`:
```bash
sudo nano /etc/nginx/sites-available/nexus-sports
```

填入以下内容（已根据您的服务器环境进行优化）：
```nginx
server {
    listen 80;
    server_name sports.everyservice.online;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name sports.everyservice.online;

    # SSL 证书路径 (由于还没运行 certbot，此处先填占位，运行后 certbot 会自动修改)
    # ssl_certificate /etc/letsencrypt/live/sports.everyservice.online/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/sports.everyservice.online/privkey.pem;

    # 继承您 jpgo 的安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;

    add_header Strict-Transport-Security "max-age=63072000" always;

    location / {
        proxy_pass http://127.0.0.1:8080; # 本项目的 Docker 前端端口
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # API 转发 (前端容器内其实已经封装了代理，此处直接转发根目录即可)
    # 如果遇到大文件上传限制，请在 server 段添加：client_max_body_size 100M;
}
```


### 2.3 启用配置
```bash
sudo ln -s /etc/nginx/sites-available/nexus-sports /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 3. 配置 SSL (HTTPS)

使用 Certbot 自动化获取 Let's Encrypt 证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d sports.everyservice.online
```
按照提示操作，选择 `2: Redirect` 将所有 HTTP 流量自动重定向到 HTTPS。

---

## 4. 自动化部署流程 (在项目目录下)

> [!NOTE]
> 在较新的 Docker 版本中，命令已从 `docker-compose` (带连字符) 升级为 `docker compose` (不带连字符)。如果提示命令找不到，请尝试后者。

1. **同步代码**: `git pull`
2. **配置环境**: `cp .env.example .env` (修改 `CORS_ORIGINS=https://sports.everyservice.online`)
3. **启动容器**: 
   ```bash
   docker compose up -d --build
   ```

4. **初始化并创建账号**:
   ```bash
   # 初始化数据库表
   docker compose exec backend python -m backend.init_db

   # 创建管理员账号 (请替换为您自己的用户名和密码)
   docker compose exec backend python -m backend.create_admin <用户名> <密码>
   ```


---

## 5. 常见问题排查

- **防火墙**: 确保 80 和 443 端口已开放：`sudo ufw allow 80`, `sudo ufw allow 443`。
- **冲突**: 若 Nginx 启动失败，检查是否有其他程序（如已有的 Docker 容器）占用了 80 端口。在这种情况下，您应该将已有容器也纳入 Nginx 反向代理管理。
- **日志**: 
  - Nginx 日志: `tail -f /var/log/nginx/error.log`
  - Docker 日.志: `docker-compose logs -f`

---
> [!TIP]
> 如果您想统一管理多个 Docker 项目，推荐使用 [Nginx Proxy Manager](https://nginxproxymanager.com/)，它提供 Web 界面来配置域名和 SSL，非常适合多域名场景。
