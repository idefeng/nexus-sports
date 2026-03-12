# Nexus Sports - 运动数据统一管理系统 (v2.0)

Nexus Sports 是一个专为个人开发者和运动爱好者设计的，用于统一管理多品牌运动轨迹（如高驰 Coros、佳明 Garmin、华为健康等）的数据聚合与分析系统。

> **核心价值**：原始数据永久冷备份、高精度轨迹解析可视化、智能去重合并、以及面向 AI 智能体（如 OpenClaw）的扩展能力。

---

## ✨ 核心特性

- **多源数据接入**：
  - **FitGpxParser**: 完美支持高驰 Coros、佳明 Garmin、Wahoo 等品牌 FIT/GPX 高级解析，自动识别设备厂商，支持 VO2max、心率、步频等核心生理指标提取。
  - **HuaweiParser**: 全面支持华为运动健康 (Huawei Health) 导出的 ZIP+JSON 结构解析，包含轨迹、配速与心率详情。
- **智能去重引擎**：基于"运动类型 + 时间窗口（±5min）"自动识别重复导入，防止冗余。
- **轨迹地图可视化**：集成 Leaflet 暗色主题地图，交互式轨迹展示，支持首尾点标记。
- **增强型活动详情页**：
  - **8 项核心指标**: 距离、时长、平均配速、各心率区间、步频、步幅、爬升、卡路里。
  - **编辑 & 备注**: 支持手动修正运动类型、距离，并可添加训练笔记。
- **批量管理与导出**：
  - **Explorer 模式**: 列表化管理，支持多选活动。
  - **ZIP 导出**: 一键打包导出选中活动的标准 GPX 轨迹。
- **极致体验 (UX)**：
  - **React Query**: 全局数据缓存与极致状态分发。
  - **骨架屏 & Toast**: 细腻的加载指示器与操作通知。
  - **全局错误处理**: 鲁棒的 ErrorBoundary，确保页面崩溃时优雅降级。
- **统计分析**：SQL 驱动的月度距离趋势、运动次数对比、运动 profile 环形图。
- **国际化 (i18n)**：中英文全量支持，包含运动术语的精准翻译。

---

## 🏗️ 系统架构

前后端分离，本地低开销运行：

| 层级 | 技术栈 |
|------|--------|
| **后端** | Python · FastAPI · SQLAlchemy 2.0 · Pydantic v2 |
| **数据库** | SQLite (默认) / 可挂载 Docker Volume |
| **前端** | React · TypeScript · Vite · TailwindCSS · React Query |
| **可视化** | Leaflet (地图) · Recharts (图表) |

---

## 🚀 快速开始

### 方式一：Docker 一键启动（推荐，生产就绪）

本地无需安装 Python/Node 即可直接运行：

```bash
# 赋予脚本权限
chmod +x deploy.sh

# 启动系统
./deploy.sh
```
- **访问入口**: [http://localhost:8080](http://localhost:8080)
- **数据存放**: 挂载在 `./backend/data` 目录。

### 方式二：Makefile 开发启动

```bash
# 一键安装
make setup

# 并行启动后端+前端
make backend  # (Terminal 1)
make frontend # (Terminal 2)
```

---

## 📂 项目结构

```text
nexus-sports/
├── backend/                # FastAPI 后端 (含 Dockerfile)
│   ├── api/endpoints/      # 业务 API (activities, stats, upload, export)
│   ├── core/               # 核心配置 (CORS, 日志, 安全)
│   ├── models/             # 数据库模型 (含 Notes, Stride Length 等)
│   ├── parsers/            # 多解析器引擎 (Factory, FitGpx, Huawei)
│   └── services/           # 持久化存储
├── webapp/                 # React 前端 (含 Dockerfile, Nginx)
│   ├── src/
│   │   ├── components/     # UI 组件 (Toast, Skeleton, ErrorBoundary)
│   │   ├── hooks/          # React QueryHooks
│   │   └── pages/          # 核心页面 (Dashboard, Stats, Explorer, Detail)
├── tests/                  # 33 个自动化测试点 (CRUD, Export, Parsers)
├── docker-compose.yml      # 全栈容器编排
├── deploy.sh               # 一键部署脚本
└── Makefile                # 研发入口
```

---

## 🛠️ 技术细节

- **Parser Factory**: 精准匹配上传的文件内容签名，自动调用相应的 Parser。
- **Idempotency**: 文件 MD5 哈希校验，配合 ImportRecord 审计日志。
- **Polyline Compression**: 运动轨迹采用 Google Polyline 算法压缩存储，减少 90% DB 体积。

---

## 🤝 贡献与反馈
本项目由 Antigravity 辅助设计并实现。如有疑问或建议，欢迎提交 Issue。
