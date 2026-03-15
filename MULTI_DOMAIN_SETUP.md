# 多域名部署指南 (Ubuntu + Docker + Nginx)

针对您已有一台运行 Docker 的 Ubuntu 服务器且需要部署多个域名的场景，本指南详细说明如何通过 **Nginx 反向代理** 实现 `sports.everyservice.online` 的部署。

## 场景假设
- 已有域名: `https://jpgo.everyservice.online/` (已在运行)
- 新域名: `https://sports.everyservice.online/`
- 系统环境: Ubuntu

---

## 1. 端口与网络准备

为了避免与现有容器冲突，本系统将使用不同的主机端口（默认为 8080 和 8000）。

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
创建文件 `/etc/nginx/sites-available/nexus-sports`:
```bash
sudo nano /etc/nginx/sites-available/nexus-sports
```

填入以下内容：
```nginx
server {
    listen 80;
    server_name sports.everyservice.online;

    location / {
        proxy_pass http://127.0.0.1:8080; # 对应前端容器映射的端口
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API 转发（前端容器内部已有代理，但如果直接访问后端可配置此处）
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/; 
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 100M;
    }
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

1. **同步代码**: `git pull`
2. **配置环境**: `cp .env.example .env` (修改 `CORS_ORIGINS=https://sports.everyservice.online`)
3. **启动容器**: `docker-compose up -d --build`

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
