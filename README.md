# Nexus Sports - 运动数据统一管理系统

Nexus Sports 是一个专为个人开发者和运动爱好者设计的，用于统一管理多品牌运动轨迹（如高驰 Coros、华为健康等）的数据聚合与分析系统。

> **核心价值**：原始数据永久冷备份、高精度轨迹解析可视化、智能去重合并、以及面向 AI 智能体（如 OpenClaw）的扩展能力。

---

## ✨ 核心特性

- **多源数据接入**：完美适配高驰（FIT/GPX）解析，预留华为（ZIP/JSON）处理逻辑。
- **轨迹地图可视化**：集成 Leaflet 暗色主题地图，Polyline 压缩存储，交互式轨迹展示。
- **智能去重引擎**：基于"运动类型 + 时间窗口（±5min）"自动识别重复导入。
- **活动详情页**：8 项运动指标（距离/时长/配速/心率/步频/步幅/爬升/卡路里）+ GPS 轨迹 + 导出 + 删除。
- **数据导出**：
  - **原始备份**：下载上传的原始 FIT/GPX 文件。
  - **GPX 导出**：基于数据库记录动态生成标准 GPX 轨迹。
- **统计分析**：月度距离趋势图、月度运动次数柱状图、运动类型分布环形图（SQL 级聚合）。
- **拖拽上传**：支持 drag & drop 上传 FIT/GPX/ZIP 文件，实时文件大小显示和状态反馈。
- **自动化能力**：
  - **Watchdog 监控**：文件夹放入新文件自动感知并入库。
  - **自动备份**：定时打包数据库与存档文件。
- **AI 智能体**：
  - Agent API 提供最新运动分析和月度报告。
  - 开放文本摘要 API，支持 Telegram/微信语音查询。
- **国际化 (i18n)**：中英文双语切换，活动类型自动中文映射（Running→跑步）。
- **安全**：CORS 可配置、上传文件大小/扩展名/魔数校验、结构化日志。

---

## 🏗️ 系统架构

前后端分离，本地低开销运行：

| 层级 | 技术栈 |
|------|--------|
| **后端** | Python · FastAPI · SQLAlchemy 2.0 · Pydantic v2 |
| **数据库** | SQLite (默认) / 可迁移 PostgreSQL |
| **前端** | React · TypeScript · Vite · TailwindCSS · React Query |
| **可视化** | Leaflet (地图) · Recharts (图表) |
| **国际化** | react-i18next |
| **任务** | Watchdog · Parser 抽象层 |

---

## 🚀 快速开始

### 使用 Makefile（推荐）

```bash
# 一键安装所有依赖
make setup

# 启动后端 (port 8000)
make backend

# 启动前端 (port 5173)
make frontend

# 运行测试
make test
```

### 手动启动

```bash
# 1. 后端
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

# 2. 前端
cd webapp && npm install && npm run dev
```

### 环境配置

复制 `.env.example` 为 `.env`，按需修改：

```bash
cp .env.example .env
```

主要配置项：`CORS_ORIGINS`、`MAX_UPLOAD_SIZE_MB`、`LOG_LEVEL`、`DATABASE_URL`。

---

## 📂 项目结构

```text
nexus-sports/
├── backend/                # FastAPI 后端
│   ├── api/endpoints/      # REST API (activities, stats, upload, agent)
│   ├── core/               # 数据库 + 配置 (CORS, 日志, 安全)
│   ├── models/             # SQLAlchemy 模型
│   ├── parsers/            # FIT/GPX 解析器 (Coros, Huawei)
│   ├── schemas/            # Pydantic v2 schemas
│   └── services/           # Watchdog, 备份服务
├── webapp/                 # React + Vite 前端
│   └── src/
│       ├── components/     # Layout, MetricCard, LanguageSwitcher
│       ├── hooks/          # React Query hooks (useQueries)
│       ├── pages/          # Dashboard, Stats, Explorer, Import, ActivityDetail, Settings
│       ├── services/       # API 调用封装 (axios)
│       ├── lib/            # i18n 配置
│       └── types/          # TypeScript 类型
├── tests/                  # pytest 测试 (21 cases)
├── .env.example            # 环境变量模板
├── Makefile                # 统一命令入口
└── requirements.txt        # Python 依赖
```

---

## 🧪 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/activities` | 分页获取活动列表 |
| GET | `/api/v1/activities/{id}` | 获取活动详情 |
| PATCH | `/api/v1/activities/{id}` | 编辑活动 |
| DELETE | `/api/v1/activities/{id}` | 删除活动 |
| POST | `/api/v1/upload` | 上传 FIT/GPX/ZIP |
| GET | `/api/v1/stats/summary` | 汇总统计 |
| GET | `/api/v1/stats/trend` | 月度趋势 (SQL 聚合) |
| GET | `/api/v1/stats/distribution` | 类型分布 |
| GET | `/api/v1/agent/latest_activity` | AI 最新分析 |
| GET | `/api/v1/agent/monthly_report` | AI 月报 |
| GET | `/api/v1/export/original/{id}` | 下载原始文件 |
| GET | `/api/v1/export/gpx/{id}` | 导出 GPX |
| GET | `/api/v1/health` | 健康检查 |

---

## 🛠️ 后续规划

- [ ] 对接高驰/华为开放 API 实现在线同步
- [ ] PostGIS 空间地理查询
- [ ] AI 训练负荷建议与周期化训练分析
- [ ] 数据加密存储
- [ ] 异步导入与进度指示

---

## 🤝 贡献与反馈
本项目由 Antigravity 辅助设计并实现。如有疑问或建议，欢迎提交 Issue。
