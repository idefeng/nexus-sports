# Nexus Sports 生产环境部署指南

本文档提供将 Nexus Sports 系统部署到正式服务器的详细操作方案。

## 1. 环境要求

在开始部署之前，请确保您的正式服务器已安装以下软件：

- **Docker**: 20.10.0+
- **Docker Compose**: 2.0.0+
- **Nginx** (可选，作为外部反向代理处理 SSL)

## 2. 部署步骤

### 2.1 获取代码
将代码上传或克隆到服务器的目标目录：
```bash
git clone <your-repository-url> /opt/nexus-sports
cd /opt/nexus-sports
```

### 2.2 配置环境变量
基于 `.env.example` 创建 `.env` 文件：
```bash
cp .env.example .env
```
**关键配置说明：**
- `ENVIRONMENT=production`: 开启生产模式。
- `CORS_ORIGINS`: 设置为您正式的域名（如 `https://sports.example.com`）。
- `DATABASE_URL`: 建议在生产环境使用 PostgreSQL（取消相关行注释），如继续使用 SQLite 请确保路径正确。
- `MAX_UPLOAD_SIZE_MB`: 根据需要调整运动数据文件上传上限。

### 2.3 启动服务
使用 Docker Compose 一键启动：
```bash
docker-compose up -d --build
```
该命令会自动：
1. 构建前端（内嵌 Nginx 服务于 8080 端口）。
2. 构建后端（FastAPI 服务于 8000 端口）。
3. 进行运行前的健康检查。

### 2.4 验证部署
检查容器运行状态：
```bash
docker-compose ps
```
确保 `nexus-sports-backend` 状态为 `(healthy)`。

## 3. SSL 证书与反向代理 (推荐)

强烈建议在生产环境使用 HTTPS。您可以使用外部 Nginx 作为网关：

**Nginx 配置示例 (`/etc/nginx/sites-enabled/nexus-sports`):**
```nginx
server {
    listen 80;
    server_name sports.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name sports.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/sports.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sports.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8080; # 转发到前端容器
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8080/api/; # 或者直接转发到后端 8000，但前端容器已有代理转发
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 4. 数据备份与维护

- **数据库**: 定期备份 `backend/data/` 目录下的 `.db` 文件。
- **日志查看**:
  ```bash
  docker-compose logs -f backend
  ```
- **更新系统**:
  ```bash
  git pull
  docker-compose up -d --build
  ```

---
## 5. 多域名冲突处理 (Ubuntu)

如果您在同一台服务器上运行多个项目（如 `sports.everyservice.online` 和其他域名），建议使用 Nginx 反向代理统一管理。

详细操作请参考：[MULTI_DOMAIN_SETUP.md](file:///Users/idefeng/DEV/nexus-sports/MULTI_DOMAIN_SETUP.md)

---
> [!IMPORTANT]
> 部署后，请务必修改默认的管理员密码（如果系统有内置初始账号）。

