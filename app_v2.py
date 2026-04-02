"""
A2UI - 极简界面，高保真预览
"""

import streamlit as st
import streamlit.components.v1 as stc
import json
import re
import importlib
import model
import components as comp_lib
importlib.reload(comp_lib)

st.set_page_config(page_title="A2UI Playground", layout="wide", initial_sidebar_state="expanded")

if 'chat_components' not in st.session_state:
    st.session_state.chat_components = []
if 'json_out' not in st.session_state:
    st.session_state.json_out = ''
if 'query' not in st.session_state:
    st.session_state.query = ''
if 'agent_text' not in st.session_state:
    st.session_state.agent_text = ''
if 'custom_components' not in st.session_state:
    st.session_state.custom_components = []
if 'edited_examples' not in st.session_state:
    st.session_state.edited_examples = {}

# ── 侧边栏导航 ──
with st.sidebar:
    st.markdown("""
    <div style="padding:4px 0 20px 0;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <div style="width:32px;height:32px;background:linear-gradient(135deg,#6366F1,#8B5CF6);border-radius:8px;display:flex;align-items:center;justify-content:center;">
                <span style="color:#fff;font-size:14px;font-weight:700;">A2</span>
            </div>
            <div>
                <div style="font-size:15px;font-weight:700;color:#F8FAFC;letter-spacing:-0.3px;">A2UI Playground</div>
                <div style="font-size:11px;color:#64748B;margin-top:1px;">MCP Provider Workbench</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("导航", ["💬 对话测试", "🧩 组件库"], label_visibility="collapsed")

    st.markdown("""
    <div style="position:fixed;bottom:16px;left:16px;right:16px;">
        <div style="font-size:10px;color:#475569;">v2.0 · Powered by Qwen</div>
    </div>
    """, unsafe_allow_html=True)

try:
    API_KEY = st.secrets["QWEN_API_KEY"]
except Exception:
    API_KEY = "Zq2YTTh5DFGtdLpETX1zJ6J8cauCH8Cn"
PROMPT = """你是智能生活助手，能够用自然语言和 UI 组件帮助用户解决问题。

根据用户的问题，输出一个 JSON 对象，包含两个字段：
- "text": 自然语言回复（1-3句话，简洁友好，像朋友对话一样）
- "components": UI 组件 JSON 数组（帮助用户完成操作，如果不需要组件可以为空数组）

【可用组件】
## 展示类
Heading - 标题 (text)
Paragraph - 段落文本 (text)
InfoTable - 信息表格 (headers: [], rows: [{name,rate,feature}])
PriceCard - 价格卡片 (items: [{label,value}], total)

## 输入/选择类
AddressInput - 地址输入 (label, placeholder, value)
ContactInput - 联系人 (label, name, phone)
TagOptions - 标签选择 (label, options: [], selected)
AmountOption - 金额选项 (label, options: [], selected)
ListOption - 列表选择 (label, options: [{title,subtitle}], selected)
Stepper - 步进器 (label, value, unit)
TextInput - 单行输入 (label, placeholder, value)
TextareaInput - 多行输入 (label, placeholder, value)
PhoneInput - 手机号输入 (label, placeholder, value)
AmountInput - 金额输入 (label, placeholder, value)

## 按钮类
ActionButton - 操作按钮组 (actions: [{label, type}])
ConfirmButton - 确认按钮 (label, disabled)
SubmitButton - 提交按钮 (label, price)
OrderButton - 下单按钮 (label, price, disabled)
PayButton - 支付按钮 (label, amount, disabled)
TextLink - 文字链接 (text, href)
AuthButton - 授权按钮 (label, agreement, checked)
VerifyButton - 核身按钮 (label, agreement, checked, idNumber)

【示例 - 用户问"帮我充话费"】
{
  "text": "好的，我来帮你充话费！请选择充值金额。",
  "components": [
    {"type": "PhoneInput", "label": "充值号码", "placeholder": "请输入手机号"},
    {"type": "AmountOption", "label": "充值金额", "options": ["¥30", "¥50", "¥100", "¥200"], "selected": 2},
    {"type": "PriceCard", "items": [{"label": "话费充值", "value": "¥100"}, {"label": "优惠减免", "value": "-¥5"}], "total": "¥95"},
    {"type": "PayButton", "label": "立即充值", "amount": "¥95"}
  ]
}

【注意】
- text 要根据用户的实际问题生成自然的对话回复
- 如果用户的问题不需要 UI 组件（如闲聊、知识问答），components 为空数组，text 中给出完整回答
- 只输出 JSON 对象，不要其他内容
"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── 基础 ── */
* { font-family: 'Inter', -apple-system, sans-serif; }
#MainMenu, footer { display: none !important; }
.stApp > header { background: transparent !important; box-shadow: none !important; }
.stApp { background: #F8F9FB; }
::-webkit-scrollbar { display: none; }

/* ── 侧边栏：暗色主题 ── */
section[data-testid="stSidebar"] {
    background: #1C1C2E !important;
    border-right: 1px solid rgba(255,255,255,0.06);
    color: #CBD5E1 !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown {
    color: #CBD5E1 !important;
}
section[data-testid="stSidebar"] .stRadio > div {
    gap: 2px;
}
section[data-testid="stSidebar"] .stRadio > div > label {
    background: transparent;
    border-radius: 8px;
    padding: 10px 14px !important;
    font-size: 13px;
    font-weight: 500;
    color: #94A3B8 !important;
    transition: all 0.15s ease;
    border: 1px solid transparent;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(255,255,255,0.05);
    color: #E2E8F0 !important;
}
section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
    background: rgba(99,102,241,0.15) !important;
    color: #A5B4FC !important;
    border-color: rgba(99,102,241,0.3);
}
/* 隐藏 radio 圆点 */
section[data-testid="stSidebar"] .stRadio > div > label > div:first-child { display: none; }

/* ── 主区域排版 ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

/* ── 输入框 ── */
.stTextArea label, .stTextInput label { display: none; }
.stTextArea textarea, .stTextInput input {
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    font-size: 13px;
    background: #fff !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}

/* ── 按钮 ── */
.stButton button {
    border: none;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.15s ease;
}
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #6366F1, #7C3AED) !important;
    color: #fff;
    box-shadow: 0 2px 8px rgba(99,102,241,0.25);
}
.stButton button[kind="primary"]:hover {
    box-shadow: 0 4px 16px rgba(99,102,241,0.35);
    transform: translateY(-1px);
}
.stButton button[kind="secondary"] {
    background: #fff !important;
    color: #374151 !important;
    border: 1px solid #E5E7EB !important;
}
.stButton button[kind="secondary"]:hover {
    background: #F9FAFB !important;
    border-color: #D1D5DB !important;
}

/* ── 代码块 ── */
.stCode { background: #1E1E2E !important; border-radius: 10px; border: 1px solid rgba(255,255,255,0.06); }
.stCode code { font-size: 11px; color: #A5B4FC; }

/* ── Expander ── */
.streamlit-expanderHeader {
    font-size: 13px !important;
    font-weight: 500;
    color: #64748B;
    background: transparent;
    border-radius: 8px;
}

/* ── 分割线 ── */
hr { border-color: #F1F5F9 !important; }

/* ── Spinner ── */
.stSpinner > div { border-color: #6366F1 transparent transparent transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── LLM prompts & helpers（组件库用） ──
EDIT_PROMPT = """你是 A2UI 组件调试助手。用户要修改一个组件的参数。

当前组件类型: {comp_type}
可用属性: {props}
当前 JSON: {current_json}

用户要求: {user_input}

请输出修改后的完整组件 JSON 对象，只输出 JSON 不要其他内容。"""

ADD_PROMPT = """你是 A2UI 组件调试助手。根据用户描述生成一个组件。

可用组件类型及属性:
{all_components}

用户描述: {user_input}

请输出完整的组件 JSON 对象（必须包含 type 字段），只输出 JSON 不要其他内容。"""

def _parse_json(raw):
    """从 LLM 输出中提取 JSON（兼容 Qwen3 think 标签和各种包装格式）"""
    s = raw.strip()
    s = re.sub(r'<think>[\s\S]*?</think>', '', s).strip()
    if '<think>' in s:
        s = s[s.index('<think>'):] if s.index('<think>') == 0 else s
        s = re.sub(r'<think>[\s\S]*', '', s).strip()
    if '```' in s:
        parts = s.split('```')
        for part in parts[1::2]:
            inner = part.strip()
            if inner.startswith('json'):
                inner = inner[4:].strip()
            try:
                return json.loads(inner)
            except json.JSONDecodeError:
                continue
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    for open_c, close_c in [('{', '}'), ('[', ']')]:
        start = s.find(open_c)
        if start == -1:
            continue
        depth = 0
        for i in range(start, len(s)):
            if s[i] == open_c:
                depth += 1
            elif s[i] == close_c:
                depth -= 1
            if depth == 0:
                try:
                    return json.loads(s[start:i+1])
                except json.JSONDecodeError:
                    break
    raise ValueError(f"无法解析 JSON: {s[:300]}")

def _preview_html(comp_json):
    """渲染单个组件的预览 HTML"""
    html = comp_lib.render_component(comp_json)
    return f'''<!DOCTYPE html><html><head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        {comp_lib.IOS_TAILWIND_CONFIG}
        {comp_lib.IOS_BASE_STYLES}
        <style>* {{ margin:0;padding:0;box-sizing:border-box; }} body {{ background:#F2F2F7;padding:12px; }} ::-webkit-scrollbar {{ display:none; }}</style>
    </head><body>{html}</body></html>'''

def _all_components_desc():
    """生成所有组件类型的简要描述（给 LLM 用）"""
    lines = []
    for name, info in comp_lib.COMPONENT_CATALOG.items():
        props = ", ".join(f"{k}: {v}" for k, v in info["props"].items())
        lines.append(f"{name} - {props}")
    return "\n".join(lines)

# ══════════════════════════════════════════════════════════
# 页面路由：基于侧边栏 radio 切换
# ══════════════════════════════════════════════════════════
if page == "💬 对话测试":
    # ── 顶部介绍区 ──
    st.markdown("""
    <div style="background:#fff; border:1px solid #E5E7EB; border-radius:14px; padding:28px 32px; margin-bottom:24px;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <div style="width:36px;height:36px;background:linear-gradient(135deg,#6366F1,#8B5CF6);border-radius:9px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <span style="color:#fff;font-size:13px;font-weight:700;">A2</span>
            </div>
            <div>
                <div style="font-size:18px; font-weight:700; color:#111827; letter-spacing:-0.4px;">A2UI Playground</div>
                <div style="font-size:12px; color:#6B7280; margin-top:1px;">AI to UI · MCP 服务方界面调试工作台</div>
            </div>
        </div>
        <div style="font-size:13px; color:#6B7280; line-height:1.7; margin-bottom:20px; max-width:720px;">
            用户向智能助手提问后，AI 自动生成结构化 JSON，客户端将其渲染为原生 UI 组件。在这里你可以模拟用户提问，实时预览 AI 生成的界面效果。
        </div>
        <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <div style="flex:1; min-width:180px; background:#F9FAFB; border-radius:10px; padding:16px 18px; border:1px solid #F3F4F6;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                    <div style="width:22px;height:22px;background:#EEF2FF;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:11px;color:#6366F1;font-weight:700;">1</div>
                    <span style="font-size:12px; font-weight:600; color:#374151;">描述场景</span>
                </div>
                <div style="font-size:11px; color:#9CA3AF; line-height:1.5;">输入用户可能的提问，如 "我要寄快递"</div>
            </div>
            <div style="flex:1; min-width:180px; background:#F9FAFB; border-radius:10px; padding:16px 18px; border:1px solid #F3F4F6;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                    <div style="width:22px;height:22px;background:#EEF2FF;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:11px;color:#6366F1;font-weight:700;">2</div>
                    <span style="font-size:12px; font-weight:600; color:#374151;">AI 生成</span>
                </div>
                <div style="font-size:11px; color:#9CA3AF; line-height:1.5;">AI 返回对话文本和 UI 组件 JSON</div>
            </div>
            <div style="flex:1; min-width:180px; background:#F9FAFB; border-radius:10px; padding:16px 18px; border:1px solid #F3F4F6;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                    <div style="width:22px;height:22px;background:#EEF2FF;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:11px;color:#6366F1;font-weight:700;">3</div>
                    <span style="font-size:12px; font-weight:600; color:#374151;">手机预览</span>
                </div>
                <div style="font-size:11px; color:#9CA3AF; line-height:1.5;">右侧模拟器实时展示最终界面效果</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 左右两栏 ──
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="section-label">设计要求</div>', unsafe_allow_html=True)

        user_query = st.text_area(
            "描述 UI 需求",
            value=st.session_state.query,
            placeholder="例如：我要寄快递，需要选择地址、包裹类型、时间",
            height=120,
            label_visibility="collapsed",
            key="query_input"
        )

        c1, c2 = st.columns([5, 1])
        with c1:
            gen = st.button("✨ 生成", use_container_width=True, type="primary")
        with c2:
            clr = st.button("✕", use_container_width=True)

        if clr:
            st.session_state.chat_components = []
            st.session_state.json_out = ''
            st.session_state.agent_text = ''
            st.session_state.query = ''
            st.rerun()

        if gen and user_query:
            st.session_state.query = user_query
            with st.spinner("生成中..."):
                raw = model.generate_with_qwen(user_query, PROMPT, API_KEY)
                if raw:
                    json_str = raw.strip()
                    json_str = re.sub(r'<think>[\s\S]*?</think>', '', json_str).strip()
                    if json_str.startswith("```"):
                        json_str = json_str.split("```")[1]
                        if json_str.startswith("json"):
                            json_str = json_str[4:]
                    json_str = json_str.strip()
                    try:
                        parsed = json.loads(json_str)
                        if isinstance(parsed, dict) and "components" in parsed:
                            st.session_state.agent_text = parsed.get("text", "")
                            st.session_state.chat_components = parsed.get("components", [])
                        elif isinstance(parsed, list):
                            st.session_state.agent_text = ""
                            st.session_state.chat_components = parsed
                        else:
                            st.session_state.agent_text = ""
                            st.session_state.chat_components = [parsed] if isinstance(parsed, dict) else []
                        st.session_state.json_out = json.dumps(st.session_state.chat_components, ensure_ascii=False, indent=2)
                    except:
                        st.session_state.agent_text = ''
                        st.session_state.chat_components = []
                        st.session_state.json_out = json_str
            st.rerun()

        if st.session_state.json_out:
            with st.expander("JSON"):
                st.code(st.session_state.json_out, language='json')

    with right:
        st.markdown('<div class="section-label">预览</div>', unsafe_allow_html=True)

        if st.session_state.chat_components or st.session_state.agent_text:
            # Dynamically render: apply library edits to chat components
            display_comps = []
            for comp in st.session_state.chat_components:
                ctype = comp.get("type", "")
                if ctype in st.session_state.edited_examples:
                    display_comps.append(st.session_state.edited_examples[ctype])
                else:
                    display_comps.append(comp)
            component_html = comp_lib.render_components(display_comps)
            chat_content = comp_lib.render_chat_html(
                st.session_state.query, st.session_state.agent_text, component_html
            )

            # iPhone 17 Pro: 393×852pt 屏幕，frame padding 10px → 413×872
            # 缩放至 320px 显示宽度: scale = 320/413 ≈ 0.775
            _SCALE = 0.775
            _FRAME_W = 413
            _FRAME_H = 872
            _DISPLAY_H = int(_FRAME_H * _SCALE) + 8

            phone = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    {comp_lib.IOS_TAILWIND_CONFIG}
    {comp_lib.IOS_BASE_STYLES}
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: transparent; }}
        ::-webkit-scrollbar {{ display: none; }}
    </style>
</head>
<body>
    <div style="
        width: {_FRAME_W}px;
        margin: 0 auto;
        transform: scale({_SCALE});
        transform-origin: top center;
    ">
        <!-- iPhone 17 Pro 外壳 -->
        <div style="
            background: linear-gradient(145deg, #1d1d1f, #2c2c2e);
            border-radius: 60px;
            padding: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        ">
            <!-- 屏幕 393×852 -->
            <div style="
                width: 393px;
                height: 852px;
                background: #fff;
                border-radius: 52px;
                overflow: hidden;
                position: relative;
                display: flex;
                flex-direction: column;
            ">
                <!-- 灵动岛 -->
                <div style="position:absolute; top:12px; left:50%; transform:translateX(-50%); width:126px; height:37px; background:#000; border-radius:20px; z-index:100;"></div>
                <!-- 状态栏 -->
                <div style="position:absolute; top:18px; left:36px; font-size:15px; font-weight:600; color:#000; z-index:99;">9:41</div>
                <div style="position:absolute; top:18px; right:32px; font-size:14px; z-index:99;">
                    <span style="margin-right:4px;">📶</span><span>🔋</span>
                </div>
                <!-- 导航栏 -->
                <div style="padding:59px 16px 12px 16px; text-align:center; font-size:17px; font-weight:600; color:#000; border-bottom:0.5px solid #C6C6C8; background:#F2F2F7; flex-shrink:0;">智能助手</div>
                <!-- 聊天区域 -->
                <div style="flex:1; overflow-y:auto; background:#F2F2F7;">
                    {chat_content}
                </div>
                <!-- 底部输入栏 -->
                <div style="padding:8px 16px; background:#F2F2F7; border-top:0.5px solid #C6C6C8; display:flex; align-items:center; gap:8px; flex-shrink:0;">
                    <div style="flex:1; background:#fff; border-radius:20px; padding:10px 16px; font-size:17px; color:#C7C7CC;">输入消息...</div>
                    <div style="width:34px; height:34px; background:#007AFF; border-radius:50%; display:flex; align-items:center; justify-content:center;">
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 14V3M8 3L3 8M8 3l5 5" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                </div>
                <!-- Home 指示条 -->
                <div style="padding:8px 0; text-align:center; flex-shrink:0; background:#F2F2F7;">
                    <div style="width:134px; height:5px; background:#000; border-radius:3px; opacity:0.25; margin:0 auto;"></div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
            stc.html(phone, height=_DISPLAY_H)
        else:
            st.markdown("""
            <div style="
                width: 320px; height: 676px; margin: 0 auto;
                background: #fff; border-radius: 46px;
                border: 1.5px dashed #D1D5DB;
                display: flex; align-items: center; justify-content: center; flex-direction: column;
                color: #9CA3AF;
            ">
                <div style="width:48px;height:48px;background:#F3F4F6;border-radius:12px;display:flex;align-items:center;justify-content:center;margin-bottom:16px;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9CA3AF" stroke-width="1.5"><rect x="5" y="2" width="14" height="20" rx="3"/><line x1="12" y1="18" x2="12" y2="18.01" stroke-width="2" stroke-linecap="round"/></svg>
                </div>
                <div style="font-size: 13px; font-weight: 500; color:#6B7280;">输入场景后生成预览</div>
                <div style="font-size: 11px; color:#D1D5DB; margin-top:4px;">iPhone 17 Pro · 393 x 852 pt</div>
            </div>
            """, unsafe_allow_html=True)

else:
    # ══════════════════════════════════════════════════════════
    # 组件库
    # ══════════════════════════════════════════════════════════
    catalog = comp_lib.COMPONENT_CATALOG
    cat_icons = {"展示类": "📋", "输入选择类": "✏️", "按钮类": "🔘"}

    st.markdown("""
    <div style="background:#fff; border:1px solid #E5E7EB; border-radius:14px; padding:20px 24px; margin-bottom:20px;">
        <div style="font-size:16px; font-weight:700; color:#111827; letter-spacing:-0.3px; margin-bottom:4px;">组件库</div>
        <div style="font-size:12px; color:#9CA3AF; line-height:1.6;">共 %d 个组件 · 点击 ✎ 按钮修改参数 · 支持自然语言描述新增组件</div>
    </div>
    """ % len(catalog), unsafe_allow_html=True)

    # 每个组件的预览高度（确保 demo 完整展示）
    _COMP_H = {
        "Heading": 60, "Paragraph": 70, "TextLink": 60,
        "ConfirmButton": 75, "SubmitButton": 75, "OrderButton": 75, "PayButton": 75,
        "ActionButton": 80,
        "Stepper": 90,
        "TextInput": 110, "PhoneInput": 110, "AmountInput": 110,
        "AddressInput": 110, "ContactInput": 110,
        "TextareaInput": 130,
        "TagOptions": 130, "AmountOption": 130,
        "AuthButton": 120, "VerifyButton": 170,
        "InfoTable": 160, "PriceCard": 190,
        "ListOption": 260,
    }
    _DEFAULT_H = 120

    # ── 编辑对话框 ──
    @st.dialog("编辑组件", width="large")
    def _edit_dialog(comp_name, is_custom=False, custom_idx=None):
        if is_custom:
            item = st.session_state.custom_components[custom_idx]
            current = item["json"]
            comp_type = current.get("type", "Unknown")
            props_desc = ", ".join(f"{k}: {v}" for k, v in catalog[comp_type]["props"].items()) if comp_type in catalog else "自定义"
        else:
            info = catalog[comp_name]
            current = st.session_state.edited_examples.get(comp_name, info["example"])
            comp_type = comp_name
            props_desc = ", ".join(f"{k}: {v}" for k, v in info["props"].items())
            is_edited = comp_name in st.session_state.edited_examples

        # 预览
        st.markdown('<div style="font-size:11px;font-weight:600;color:#9CA3AF;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">Preview</div>', unsafe_allow_html=True)
        stc.html(_preview_html(current), height=_COMP_H.get(comp_type, _DEFAULT_H))

        # 当前 JSON
        with st.expander("当前 JSON", expanded=False):
            st.code(json.dumps(current, ensure_ascii=False, indent=2), language='json')

        # 修改输入
        edit_val = st.text_area("修改描述", placeholder="用自然语言描述你想要的修改，例如：\n- 把标题改成「会员充值」\n- 增加一个 ¥500 的选项\n- 把按钮改成禁用状态", height=100, key="dialog_edit_input")

        # 按钮行
        btn_cols = st.columns([1, 1, 1] if (not is_custom and is_edited) else [1, 1])
        with btn_cols[0]:
            do_submit = st.button("确认修改", type="primary", use_container_width=True, disabled=not edit_val)
        with btn_cols[1]:
            if is_custom:
                do_delete = st.button("删除组件", use_container_width=True)
            else:
                do_delete = False
        if not is_custom and is_edited:
            with btn_cols[2]:
                if st.button("还原默认", use_container_width=True):
                    del st.session_state.edited_examples[comp_name]
                    st.rerun()

        if do_submit and edit_val:
            prompt = EDIT_PROMPT.format(comp_type=comp_type, props=props_desc, current_json=json.dumps(current, ensure_ascii=False), user_input=edit_val)
            with st.spinner("AI 正在修改..."):
                raw = model.generate_with_qwen(edit_val, prompt, API_KEY)
            if raw:
                try:
                    new_json = _parse_json(raw)
                    if is_custom:
                        st.session_state.custom_components[custom_idx]["json"] = new_json
                    else:
                        st.session_state.edited_examples[comp_name] = new_json
                    st.rerun()
                except Exception as ex:
                    st.error(f"解析失败：{ex}")
            else:
                st.error("模型调用失败")

        if is_custom and do_delete:
            st.session_state.custom_components.pop(custom_idx)
            st.rerun()

    # ── 新增组件（轻量一行） ──
    ac1, ac2 = st.columns([6, 1], gap="small")
    with ac1:
        add_desc = st.text_input("新增", placeholder="用自然语言描述组件，如：一个显示会员到期提醒的警告通知", label_visibility="collapsed", key="add_comp_input")
    with ac2:
        add_btn = st.button("+ 新增", use_container_width=True, type="primary", key="add_comp_btn")

    if add_btn and add_desc:
        with st.spinner("生成中..."):
            prompt = ADD_PROMPT.format(all_components=_all_components_desc(), user_input=add_desc)
            raw = model.generate_with_qwen(add_desc, prompt, API_KEY)
            if raw:
                try:
                    comp_json = _parse_json(raw)
                    st.session_state.custom_components.append({"json": comp_json, "desc": add_desc})
                    st.rerun()
                except Exception as ex:
                    st.error(f"解析失败：{ex}")
                    with st.expander("原始输出"):
                        st.code(raw[:1000], language="text")
            else:
                st.error("模型调用失败")

    # ── 自定义组件 ──
    if st.session_state.custom_components:
        st.markdown("""
        <div style="margin:16px 0 8px 0; padding:10px 16px; background:#ECFDF5; border:1px solid #D1FAE5; border-radius:10px; display:flex; align-items:center; gap:8px;">
            <span style="font-size:13px; font-weight:600; color:#065F46;">自定义组件</span>
            <span style="font-size:11px; background:#D1FAE5; color:#065F46; padding:2px 10px; border-radius:6px; font-weight:500;">%d</span>
        </div>
        """ % len(st.session_state.custom_components), unsafe_allow_html=True)

        for i, item in enumerate(st.session_state.custom_components):
            comp_json = item["json"]
            comp_type = comp_json.get("type", "Unknown")

            col_info, col_preview, col_btn = st.columns([3, 2, 0.3], gap="small")
            with col_info:
                st.markdown(f'''
                <div style="padding:12px 0;">
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                        <code style="font-size:13px;font-weight:600;color:#111827;background:transparent;padding:0;">{comp_type}</code>
                        <span style="width:6px;height:6px;background:#10B981;border-radius:50%;display:inline-block;" title="自定义"></span>
                    </div>
                    <div style="font-size:11px;color:#9CA3AF;line-height:1.6;">{item["desc"]}</div>
                </div>
                ''', unsafe_allow_html=True)
            with col_preview:
                stc.html(_preview_html(comp_json), height=_COMP_H.get(comp_type, _DEFAULT_H))
            with col_btn:
                if st.button("✎", key=f"ce_{i}", help="编辑组件"):
                    _edit_dialog(comp_type, is_custom=True, custom_idx=i)

            st.markdown('<div style="height:1px;background:#F3F4F6;margin:0;"></div>', unsafe_allow_html=True)

    # ── 按分类展示组件 ──
    seen_cats = []
    for v in catalog.values():
        if v["category"] not in seen_cats:
            seen_cats.append(v["category"])

    for cat in seen_cats:
        cat_items = {k: v for k, v in catalog.items() if v["category"] == cat}
        if not cat_items:
            continue

        count = len(cat_items)
        st.markdown(f'''
        <div style="margin:20px 0 8px 0; padding:10px 16px; background:#fff; border:1px solid #E5E7EB; border-radius:10px; display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:14px;">{cat_icons.get(cat, "")}</span>
                <span style="font-size:13px; font-weight:600; color:#374151;">{cat}</span>
            </div>
            <span style="font-size:11px; background:#F3F4F6; color:#6B7280; padding:2px 10px; border-radius:6px; font-weight:500;">{count}</span>
        </div>
        ''', unsafe_allow_html=True)

        for comp_name, info in cat_items.items():
            current_example = st.session_state.edited_examples.get(comp_name, info["example"])
            is_edited = comp_name in st.session_state.edited_examples

            props_tags = " ".join(
                f'<span style="display:inline-block;background:#F3F4F6;color:#6B7280;padding:2px 8px;border-radius:5px;font-size:10px;font-family:\'SF Mono\',monospace;font-weight:500;">{k}</span>'
                for k in info["props"].keys()
            )
            edited_dot = '<span style="width:6px;height:6px;background:#F59E0B;border-radius:50%;display:inline-block;margin-left:4px;" title="已修改"></span>' if is_edited else ''

            col_info, col_preview, col_btn = st.columns([3, 2, 0.3], gap="small")

            with col_info:
                st.markdown(f'''
                <div style="padding:12px 0;">
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                        <code style="font-size:13px;font-weight:600;color:#111827;background:transparent;padding:0;">{comp_name}</code>{edited_dot}
                    </div>
                    <div style="font-size:11px;color:#9CA3AF;line-height:1.6;margin-bottom:8px;">{info["description"]}</div>
                    <div style="display:flex;flex-wrap:wrap;gap:4px;">{props_tags}</div>
                </div>
                ''', unsafe_allow_html=True)

            with col_preview:
                stc.html(_preview_html(current_example), height=_COMP_H.get(comp_name, _DEFAULT_H))

            with col_btn:
                if st.button("✎", key=f"e_{comp_name}", help="编辑组件"):
                    _edit_dialog(comp_name)

            st.markdown('<div style="height:1px;background:#F3F4F6;margin:0;"></div>', unsafe_allow_html=True)