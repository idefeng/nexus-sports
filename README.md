# Nexus Sports - 运动数据统一管理系统

Nexus Sports 是一个专为个人开发者和运动爱好者设计的，用于统一管理多品牌运动轨迹（如高驰 Coros、华为健康等）的数据聚合与分析系统。

> **核心价值**：原始数据永久冷备份、高精度轨迹解析可视化、智能去重合并、以及面向 AI 智能体（如 OpenClaw）的扩展能力。

---

## ✨ 核心特性

- **多源数据接入**：目前完美适配高驰（FIT/GPX）解析，并预留了华为（ZIP/JSON）处理逻辑。
- **轨迹地图可视化**：集成 Leaflet/Folium，通过 Polyline 压缩存储，通过前端实现高精度交互式轨迹回放。
- **智能去重引擎**：基于“运动类型 + 时间窗口（±5min）”自动识别重复导入，保障数据统计的准确性。
- **数据导出与备份**：
  - **原始备份**：支持下载当初上传的原始文件。
  - **GPX 导出**：基于数据库记录动态逆向生成标准的 GPX 轨迹。
- **自动化能力**：
  - **Watchdog 监控**：指定文件夹内放入新文件，系统自动感知并后台静默入库。
  - **自动备份**：定时任务一键打包数据库与存档文件。
- **AI 智能体友好**：
  - 提供 `NEXUS_SPORTS_SKILL.md` 配置声明。
  - 开放专为大模型优化的文本摘要 API，支持通过 Telegram/微信 语音查询跑量与周报。

---

## 🏗️ 系统架构

系统采用前后端分离架构，专为本地低开销运行优化：

- **后端 (Backend)**: Python + FastAPI + SQLAlchemy
- **数据库 (Database)**: SQLite (默认) / 可一键迁移至 PostgreSQL
- **前端 (Frontend)**: Streamlit + Plotly + Folium
- **任务处理**: 同步/异步 Parser 抽象层 + Watchdog 后台常驻脚本

---

## 🚀 快速开始

### 1. 环境准备
确保系统已安装 Python 3.9+。

```bash
# 进入项目目录并创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 初始化数据库
```bash
PYTHONPATH=. python backend/init_db.py
```

### 3. 启动服务
建议在两个独立的终端中分别运行后端与前端：

**启动后端 API:**
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

**启动前端 Web UI:**
```bash
streamlit run frontend/app.py
```

### 4. (可选) 启动自动化导入监控
如果你希望放入文件夹即导入，请运行：
```bash
python backend/services/watcher.py --dir ./path/to/your/sync/folder
```

---

## 📂 项目结构

```text
nexus-sports/
├── backend/                # FastAPI 后端核心
│   ├── api/                # API 路由与接口定义
│   ├── core/               # 数据库配置与系统设置
│   ├── models/             # SQLAlchemy 数据库模型
│   ├── parsers/            # 品牌适配层 (Coros, Huawei 等)
│   ├── services/           # 存储、备份、监控等独立服务
│   └── utils/              # 加密、补丁、迁移等工具类
├── frontend/               # Streamlit 前端
│   ├── app.py              # 主看板页面
│   └── pages/              # 统计图表、轨迹详情等子页面
├── data/                   # 本地存储 (数据库、存档文件、备份)
├── docs/                   # 设计文档与技术方案
├── requirements.txt        # 依赖列表
└── NEXUS_SPORTS_SKILL.md   # OpenClaw AI 技能描述
```

---

## 🛠️ 后续规划

- [ ] 对接华为/高驰开放 API 实现自动在线同步。
- [ ] 启用 GIS 扩展 (PostGIS) 进行更复杂的空间地理查询。
- [ ] 基于历史运动数据，结合大模型提供更专业的训练负荷建议。

---

## 🤝 贡献与反馈
本项目由 Antigravity 辅助设计并实现。如有疑问或建议，欢迎提交 Issue。
