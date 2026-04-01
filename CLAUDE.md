# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

基于 Streamlit 构建的**金融/生活 AI 助手**测试工具。使用 Qwen 和 Gemini 模型生成 HTML 响应，在手机模拟器中预览效果。用于测试和优化支付宝生活助手的 AI 生成响应。

## 常用命令

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行 Streamlit 应用
streamlit run app.py          # 主应用：Prompt 测试工具
streamlit run app_v2.py       # A2UI：JSON 组件生成器
streamlit run render_10_case.py  # 渲染对比：并排比较多个版本

# 运行批量处理脚本
python refine_answer.py       # 使用 Gemini + Google Search 批量优化
python 50_query_process.py    # 50条查询处理
```

## 架构

### 模型层 (`model.py`)

统一封装两个 AI 模型的调用：
- `generate_with_qwen()` — OpenAI 兼容 API，默认调用 Qwen3-235B
- `generate_with_gemini()` — Google Gemini API

**环境变量配置：**
- `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `DEFAULT_MODEL` — Qwen 配置
- `GEMINI_API_KEY` / `GEMINI_PROXY` — Gemini 配置

默认 Base URL: `https://antchat.alipay.com/v1`

### UI 层

两个独立的 Streamlit 应用：

**`app.py`** — Prompt 测试工具
- 从 `prompt/*.md` 加载系统提示词
- 支持自定义 API 密钥和端点
- 输入 Query + 上下文，生成 HTML 并在手机模拟器中预览
- 每小时 10 次请求频率限制

**`app_v2.py`** — A2UI 组件生成器
- 根据自然语言描述生成 UI 组件 JSON
- 调用 `components.py` 渲染为移动端 HTML
- 实时预览生成的界面

### 组件库 (`components.py`)

移动端 Tailwind 风格的 UI 组件渲染器，包含 40+ 组件：

- **展示类**: ServiceCard, AddressItem, PackageInfo, PriceDetail, Timeline, Notice, Coupon
- **输入/选择类**: AddressInput, ContactInput, PackageSelector, WeightSelector, TimePicker
- **意图澄清组件**: TagOptions, AmountOption, ListOption, Stepper, TextInput, AmountInput
- **按钮类**: ConfirmButton, OrderButton, PayButton, AuthButton, VerifyButton

核心函数：
- `render_component(comp)` — 渲染单个组件
- `render_components(components)` — 渲染组件列表
- `wrap_html(content)` — 包装完整 HTML 文档

### 批量处理 (`refine_answer.py`)

使用 Gemini + Google Search 优化回答：
- 从 CSV/Excel 读取测试用例（列名：`query`, `前1`, `中间8`, `后1`, `修改意见`）
- 生成结果追加到新列（格式：`8部分内容_MMDD_HHMM`）
- 支持断点续传，自动跳过已生成行

### 数据文件 (`data_files/`)

测试数据格式：
- 必须包含 `query` 列
- 可选列：`前1`, `中间8`, `后1`, `修改意见`
- 支持 `.csv` 和 `.xlsx` 格式

## 重要路径

- 核心测试数据: `data_files/core_test_case.csv`
- 默认提示词: `prompt/sp_for_50_query_1230.md`
- 带 Google Search 的提示词: `prompt/sp_CSS_with_search.md`

## 归档目录

废弃文件移至 `archive/`，包括旧版本脚本、临时文件和历史数据。