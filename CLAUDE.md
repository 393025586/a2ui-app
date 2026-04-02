# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

基于 Streamlit 构建的**支付宝生活助手** AI 响应测试工具。使用 Qwen 和 Gemini 模型生成移动端 UI，在手机模拟器中预览。有两条核心流水线：HTML 直出（app.py）和 JSON 组件化（app_v2.py）。

## 常用命令

```bash
source .venv/bin/activate

# Streamlit 应用（默认端口 8501）
streamlit run app.py              # Prompt 测试：HTML 直出 + 手机预览
streamlit run app_v2.py           # A2UI Playground：JSON 组件生成 + 组件库管理
streamlit run render_10_case.py   # 10 条用例并排对比渲染

# 批量处理
python refine_answer.py           # Gemini + Google Search 批量优化
python 50_query_process.py        # 50 条查询顺序处理（Qwen）
```

## 架构

### 数据流

```
app.py:    Query + System Prompt → Qwen/Gemini → 原始 HTML → 手机模拟器预览
app_v2.py: Query → Qwen → JSON 组件数组 → components.py 渲染 → chat 气泡 UI 预览
```

### 模型层 (`model.py`)

统一封装两个 AI 模型，懒初始化客户端：
- `generate_with_qwen()` — OpenAI 兼容 API（默认 Qwen3-235B，端点 `antchat.alipay.com/v1`）
- `generate_with_gemini()` — Google genai SDK（gemini-2.5-flash）

**环境变量：** `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `DEFAULT_MODEL`（Qwen），`GEMINI_API_KEY` / `GEMINI_PROXY`（Gemini）

### UI 层

**`app.py`** — Prompt 测试工具
- 从 `prompt/*.md` 加载系统提示词，左栏输入右栏手机预览
- 每小时 10 次请求频率限制

**`app_v2.py`** — A2UI 组件生成器（双 Tab）
- Tab 1（对话模式）：LLM 返回 JSON 组件数组 → `components.py` 渲染为 HTML → `render_chat_html()` 包装成气泡 UI
- Tab 2（组件库）：浏览 `COMPONENT_CATALOG`，支持内联编辑/新增/删除组件，编辑后实时同步到 Tab 1 预览
- **关键技术细节：** LLM 返回的 JSON 需先剥离 Qwen3 的 `<think>...</think>` 标签和 markdown 代码围栏，再做 JSON 解析

### 组件库 (`components.py`)

移动端 Tailwind 风格的 UI 组件渲染器（40+ 组件），核心机制：
- `RENDERERS` 字典：组件类型 → `render_xxx()` 函数的动态分发
- `COMPONENT_CATALOG`：每个组件的 scope/category/description/props/example 元数据，供 LLM 生成时参考
- `render_component(comp)` / `render_components(components)` — 单个/批量渲染
- `wrap_html(content)` — 完整 HTML 文档包装（含 Tailwind CDN）
- `render_chat_html(user_query, agent_text, component_html)` — 聊天气泡界面

添加新组件：写 `render_xxx()` 函数 → 加入 `RENDERERS` 字典 → 在 `COMPONENT_CATALOG` 中注册元数据。

### 对比渲染 (`render_10_case.py`)

从 `data_files/10goodcase.csv` 读取用例，生成 4 列并排手机模拟器（375×812px），内含完整 HTML/CSS 模板（Chat 气泡、表格横向滚动、Chart.js 支持）。模板使用占位符 `__QUERY__`、`__INTRO_BLOCK__`、`__MAIN_CONTENT__`、`__OUTRO_BLOCK__`。

### 批量处理

- **`refine_answer.py`**：Gemini + Google Search 优化，从 CSV/Excel 读取（列：`query`, `前1`, `中间8`, `后1`, `修改意见`），结果列名格式 `8部分内容_MMDD_HHMM`，支持断点续传
- **`50_query_process.py`**：Qwen 顺序处理，60s 间隔，逐行持久化

### 数据文件 (`data_files/`)

测试数据格式：必须包含 `query` 列，可选 `前1`/`中间8`/`后1`/`修改意见`，支持 `.csv` 和 `.xlsx`。

## 注意事项

- `prompt/`、`data_files/`、`archive/`、`backup_*/` 均在 `.gitignore` 中，不会被提交
- 废弃文件移至 `archive/`，旧版本备份在 `backup_v1/`、`backup_v2/`
- Streamlit 主题配置在 `.streamlit/config.toml`（主色 #007AFF）
- 依赖：`openai`、`streamlit`、`google-genai`（见 `requirements.txt`）