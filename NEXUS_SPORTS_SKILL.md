# Nexus Sports Skill for OpenClaw

This document defines the interface and instructions for OpenClaw agents to interact with the Nexus Sports personal fitness database. You can directly copy these instructions into your OpenClaw agent's `SOUL.md` or tools configuration.

## 🤖 Agent Instructions (Prompt)

```markdown
当你需要查询用户的运动数据（如跑量、最近一次活动、消耗的卡路里）时，请使用以下 REST API 端点向本地 Nexus Sports 服务器发起请求。

**API Base URL**: `http://localhost:8000/api/v1/agent`

**可用接口**:

1. **查询最近一次运动**:
   - **Method**: `GET`
   - **Endpoint**: `/latest_activity`
   - **用途**: 获取用户最后一次运动的时间、类型、距离、时长和能量消耗的自然语言摘要。
   - **返回格式**: JSON 包含一个 `report` 字段（包含直接可回答给用户的摘要段落）和一个 `raw_data` 字段（方便你自己做二次计算）。

2. **查询月度汇总报告**:
   - **Method**: `GET`
   - **Endpoint**: `/monthly_report`
   - **Query Params**: `target_month` (可选, 格式 `YYYY-MM`，如 `2026-03`。如果不传则默认当月)。
   - **用途**: 获取用户在一个月内的总里程、总次数、最常进行的运动及其摘要。
   - **返回格式**: JSON 包含一个 `report` 字段（包含阅读友好的月度摘要）和 `metrics` 字段（包含详细数字）。

**回复准则**: 
- 当调用这些接口成功后，你可以直接使用 `report` 字段中的文本向用户进行汇报，或者根据 `raw_data` / `metrics` 字段结合用户的具体问题（例如“我这周跑了多少公里”）来自己推算和总结。
- 如果接口返回错误或者无法连接（如服务器未启动），请礼貌地告知用户服务器可能离线。
```

## 🛠️ OpenClaw Tool Definitons (Optional JSON Schema)
If your OpenClaw configuration supports strict JSON tool calls:

```json
[
  {
    "type": "function",
    "function": {
      "name": "get_latest_activity",
      "description": "Fetch the summary of the user's most recent fitness activity.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_monthly_report",
      "description": "Fetch aggregated fitness statistics for a specific month.",
      "parameters": {
        "type": "object",
        "properties": {
          "target_month": {
            "type": "string",
            "description": "The target month in YYYY-MM format, e.g., '2026-03'. Leave empty for current month."
          }
        }
      }
    }
  }
]
```
