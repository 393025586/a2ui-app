"""
A2UI - 极简界面，高保真预览
"""

import streamlit as st
import streamlit.components.v1 as stc
import json
import model
import components as comp_lib

st.set_page_config(page_title="A2UI Playground", layout="wide", initial_sidebar_state="collapsed")

if 'preview' not in st.session_state:
    st.session_state.preview = ''
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
ServiceCard - 服务卡片 (icon, title, subtitle, tag)
AddressItem - 地址展示 (type, name, phone, address, icon)
PackageInfo - 包裹信息 (weight, type, value)
PriceDetail - 价格明细 (items: [{label,value}], total)
Timeline/StepProgress - 进度条 (steps: [], current)
Notice - 提示 (type: info/warning/success, title, content)
Coupon - 优惠券 (title, amount, condition, deadline)

## 输入/选择类
AddressInput - 地址输入 (label, placeholder, icon)
ContactInput - 联系人 (label, name, phone)
PackageSelector - 包裹类型 (options: [], selected)
WeightSelector - 重量 (label, value, unit)
TimePicker - 时间选择 (label, slots: [])

## 意图澄清组件
TagOptions - 标签选择 (label, options: [], selected)
AmountOption - 金额选项 (label, options: [], selected)
ListOption - 列表选择 (label, options: [{title,subtitle,icon}])
Stepper - 步进器 (label, value, min, max, unit)
TextInput - 单行输入 (label, placeholder, value)
TextareaInput - 多行输入 (label, placeholder, rows)
PhoneInput - 手机号输入 (label, placeholder, value)
AmountInput - 金额输入 (label, placeholder, value)

## 按钮类
ConfirmButton - 确认按钮 (label)
TextLink - 文字链接 (text, href)
OrderButton - 下单按钮 (label, price, originalPrice)
SubmitButton - 提交按钮 (label, price)
PayButton - 支付按钮 (label, amount)
AuthButton - 授权按钮 (label, agreement, checked)
VerifyButton - 核身按钮 (label, agreement, idNumber)

## 特定信息
AddressCollector - 地址收集 (type, name, phone, address, fromBook)

【示例 - 用户问"我要寄快递"】
{
  "text": "好的，我来帮你寄快递！请填写以下信息，我会为你预估费用。",
  "components": [
    {"type": "StepProgress", "steps": ["下单","取件","运输","签收"], "current": 0},
    {"type": "AddressCollector", "type": "寄件", "name": "", "phone": "", "address": ""},
    {"type": "AddressCollector", "type": "收件", "name": "", "phone": "", "address": ""},
    {"type": "PackageSelector", "options": ["文件", "物品", "生鲜", "数码"]},
    {"type": "Stepper", "label": "包裹重量", "value": 1, "unit": "kg"},
    {"type": "TimePicker", "label": "期望取件时间", "slots": ["09:00-11:00", "14:00-16:00"]},
    {"type": "PriceDetail", "items": [{"label":"基础运费","value":"¥12"},{"label":"包装费","value":"¥3"}], "total": "¥15"},
    {"type": "OrderButton", "label": "确认下单", "price": "¥15"}
  ]
}

【注意】
- text 要根据用户的实际问题生成自然的对话回复
- 如果用户的问题不需要 UI 组件（如闲聊、知识问答），components 为空数组，text 中给出完整回答
- 只输出 JSON 对象，不要其他内容
"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', -apple-system, sans-serif; }
#MainMenu, footer, header, .stApp > header { display: none !important; }

/* 标题 */
.app-title { font-size: 20px; font-weight: 700; color: #0F172A; margin-bottom: 12px; }
.section-label { font-size: 11px; font-weight: 600; color: #64748B; text-transform: uppercase; margin-bottom: 8px; }

/* 输入框 */
.stTextArea label, .stTextInput label { display: none; }
.stTextArea textarea, .stTextInput input {
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    font-size: 13px;
}

/* 按钮 */
.stButton button {
    border: none;
    border-radius: 8px;
    background: #1677FF;
    color: #fff;
    font-size: 13px;
    font-weight: 600;
}

/* JSON */
.stCode { background: #1E293B; border-radius: 8px; border: none; }
.stCode code { font-size: 11px; color: #94A3B8; }

/* 隐藏滚动条 */
::-webkit-scrollbar { display: none; }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown('<div class="app-title">A2UI Playground</div>', unsafe_allow_html=True)

# Tab 布局
tab_chat, tab_lib = st.tabs(["对话测试", "组件库"])

# ══════════════════════════════════════════════════════════
# Tab 1: 对话测试（原有功能）
# ══════════════════════════════════════════════════════════
with tab_chat:
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
            st.session_state.preview = ''
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
                    if json_str.startswith("```"):
                        json_str = json_str.split("```")[1]
                        if json_str.startswith("json"):
                            json_str = json_str[4:]
                    json_str = json_str.strip()
                    try:
                        parsed = json.loads(json_str)
                        if isinstance(parsed, dict) and "components" in parsed:
                            agent_text = parsed.get("text", "")
                            components = parsed.get("components", [])
                        elif isinstance(parsed, list):
                            agent_text = ""
                            components = parsed
                        else:
                            agent_text = ""
                            components = [parsed] if isinstance(parsed, dict) else []
                        st.session_state.agent_text = agent_text
                        st.session_state.json_out = json.dumps(components, ensure_ascii=False, indent=2)
                        component_html = comp_lib.render_components(components)
                        st.session_state.preview = comp_lib.render_chat_html(
                            user_query, agent_text, component_html
                        )
                    except:
                        st.session_state.agent_text = ''
                        st.session_state.json_out = json_str
                        st.session_state.preview = '<div>JSON 解析错误</div>'
            st.rerun()

        if st.session_state.json_out:
            with st.expander("JSON"):
                st.code(st.session_state.json_out, language='json')

    with right:
        st.markdown('<div class="section-label">预览</div>', unsafe_allow_html=True)

        if st.session_state.preview:
            phone = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, "SF Pro Text", sans-serif; background: transparent; }}
        ::-webkit-scrollbar {{ display: none; }}
    </style>
</head>
<body>
    <div style="
        width: 320px;
        margin: 0 auto;
        background: linear-gradient(145deg, #2a2a3e, #1a1a2e);
        border-radius: 50px;
        padding: 10px;
        box-shadow: 0 30px 80px rgba(0,0,0,0.3);
    ">
        <div style="
            width: 100%;
            height: 600px;
            background: #fff;
            border-radius: 42px;
            overflow: hidden;
            position: relative;
            display: flex;
            flex-direction: column;
        ">
            <!-- 灵动岛 -->
            <div style="position: absolute; top: 16px; left: 50%; transform: translateX(-50%); width: 90px; height: 26px; background: #000; border-radius: 14px; z-index: 100;"></div>
            <!-- 状态栏 -->
            <div style="position: absolute; top: 20px; left: 40px; font-size: 13px; font-weight: 600; color: #000; z-index: 99;">9:41</div>
            <div style="position: absolute; top: 20px; right: 36px; font-size: 12px; z-index: 99;">📶 🔋</div>
            <!-- 导航栏 -->
            <div style="padding: 52px 0 8px 0; text-align: center; font-size: 14px; font-weight: 600; color: #1f2937; border-bottom: 0.5px solid #e5e7eb; background: #f7f7f7; flex-shrink: 0;">智能助手</div>
            <!-- 聊天内容 -->
            <div style="flex: 1; overflow-y: auto; background: #EDEDED;">
                {st.session_state.preview}
            </div>
            <!-- 底部输入栏 -->
            <div style="padding: 8px 10px; background: #f7f7f7; border-top: 0.5px solid #e5e7eb; display: flex; align-items: center; gap: 8px; flex-shrink: 0;">
                <div style="flex: 1; background: #fff; border-radius: 4px; padding: 6px 10px; font-size: 12px; color: #bbb;">输入消息...</div>
                <div style="width: 28px; height: 28px; background: #07C160; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #fff;">></div>
            </div>
            <!-- Home 条 -->
            <div style="padding: 6px 0; text-align: center; flex-shrink: 0; background: #f7f7f7;">
                <div style="width: 120px; height: 4px; background: #000; border-radius: 2px; opacity: 0.3; margin: 0 auto;"></div>
            </div>
        </div>
    </div>
</body>
</html>'''
            stc.html(phone, height=680)
        else:
            st.markdown("""
            <div style="
                width: 320px; height: 600px; margin: 0 auto;
                background: #F1F3F4; border-radius: 42px;
                border: 2px dashed #CBD5E1;
                display: flex; align-items: center; justify-content: center; flex-direction: column;
                color: #94A3B8;
            ">
                <div style="font-size: 40px; opacity: 0.4; margin-bottom: 12px;">📱</div>
                <div style="font-size: 12px;">输入需求后预览</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# Tab 2: 组件库
# ══════════════════════════════════════════════════════════

# LLM prompts for component editing/creation
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
    """从 LLM 输出中提取 JSON"""
    s = raw.strip()
    if s.startswith("```"):
        s = s.split("```")[1]
        if s.startswith("json"):
            s = s[4:]
    return json.loads(s.strip())

def _preview_html(comp_json):
    """渲染单个组件的预览 HTML"""
    html = comp_lib.render_component(comp_json)
    return f'''<!DOCTYPE html><html><head>
        <meta charset="UTF-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>* {{ margin:0;padding:0;box-sizing:border-box; }} body {{ font-family:-apple-system,sans-serif;background:#F8FAFC;padding:10px; }} ::-webkit-scrollbar {{ display:none; }}</style>
    </head><body>{html}</body></html>'''

def _all_components_desc():
    """生成所有组件类型的简要描述（给 LLM 用）"""
    lines = []
    for name, info in comp_lib.COMPONENT_CATALOG.items():
        props = ", ".join(f"{k}: {v}" for k, v in info["props"].items())
        lines.append(f"{name} - {props}")
    return "\n".join(lines)

with tab_lib:
    catalog = comp_lib.COMPONENT_CATALOG
    cat_icons = {"展示类": "📋", "输入选择类": "✏️", "按钮类": "🔘", "特殊组件": "⚙️"}

    # ── 新增组件区 ──
    st.markdown('''
    <div style="padding:12px 16px;background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;margin-bottom:8px;">
        <span style="font-size:14px;font-weight:700;color:#166534;">+ 新增组件</span>
        <span style="font-size:12px;color:#4ADE80;margin-left:8px;">用自然语言描述你想要的组件</span>
    </div>
    ''', unsafe_allow_html=True)

    add_col1, add_col2 = st.columns([5, 1])
    with add_col1:
        add_desc = st.text_input("描述组件", placeholder="例如：一个显示会员到期提醒的警告通知", label_visibility="collapsed", key="add_comp_input")
    with add_col2:
        add_btn = st.button("生成", use_container_width=True, type="primary", key="add_comp_btn")

    if add_btn and add_desc:
        with st.spinner("生成中..."):
            prompt = ADD_PROMPT.format(all_components=_all_components_desc(), user_input=add_desc)
            raw = model.generate_with_qwen(add_desc, prompt, API_KEY)
            if raw:
                try:
                    comp_json = _parse_json(raw)
                    st.session_state.custom_components.append({
                        "name": comp_json.get("type", "Custom") + f"_{len(st.session_state.custom_components)+1}",
                        "json": comp_json,
                        "desc": add_desc,
                    })
                    st.rerun()
                except:
                    st.error("生成失败，请重试")

    # ── 自定义组件列表 ──
    if st.session_state.custom_components:
        st.markdown('''
        <div style="margin:12px 0 4px 0;padding:16px 20px;background:#F0FDF4;border-left:3px solid #22C55E;border-radius:0 8px 8px 0;">
            <span style="font-size:16px;font-weight:700;color:#0F172A;">自定义组件</span>
            <span style="font-size:12px;color:#64748B;margin-left:8px;">通过自然语言生成的组件</span>
        </div>
        ''', unsafe_allow_html=True)

        to_delete = None
        for i, item in enumerate(st.session_state.custom_components):
            col_info, col_preview, col_del = st.columns([3, 2, 0.3], gap="medium")
            comp_json = item["json"]
            comp_type = comp_json.get("type", "Unknown")

            with col_info:
                st.markdown(f'''
                <div style="padding:12px 0;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                        <span style="font-size:14px;font-weight:700;color:#0F172A;font-family:monospace;">{comp_type}</span>
                        <span style="font-size:10px;background:#DCFCE7;color:#166534;padding:2px 8px;border-radius:10px;">自定义</span>
                    </div>
                    <div style="font-size:12px;color:#64748B;line-height:1.6;margin-bottom:6px;">{item["desc"]}</div>
                    <code style="font-size:10px;color:#94A3B8;">{json.dumps(comp_json, ensure_ascii=False)}</code>
                </div>
                ''', unsafe_allow_html=True)

            with col_preview:
                stc.html(_preview_html(comp_json), height=90)

            with col_del:
                if st.button("✕", key=f"del_custom_{i}"):
                    to_delete = i

            # 自定义组件的编辑区
            with st.expander(f"调试 {comp_type}", expanded=False):
                ec1, ec2 = st.columns([3, 2], gap="medium")
                with ec1:
                    edit_input = st.text_input("描述修改", placeholder="例如：把内容改成双十一活动", key=f"edit_custom_{i}", label_visibility="collapsed")
                    eb1, eb2 = st.columns(2)
                    with eb1:
                        if st.button("应用修改", key=f"apply_custom_{i}", use_container_width=True, type="primary") and edit_input:
                            props_desc = ""
                            if comp_type in catalog:
                                props_desc = ", ".join(f"{k}: {v}" for k, v in catalog[comp_type]["props"].items())
                            prompt = EDIT_PROMPT.format(comp_type=comp_type, props=props_desc or "自定义", current_json=json.dumps(comp_json, ensure_ascii=False), user_input=edit_input)
                            with st.spinner("修改中..."):
                                raw = model.generate_with_qwen(edit_input, prompt, API_KEY)
                                if raw:
                                    try:
                                        st.session_state.custom_components[i]["json"] = _parse_json(raw)
                                        st.rerun()
                                    except:
                                        st.error("修改失败")
                    st.code(json.dumps(comp_json, ensure_ascii=False, indent=2), language="json")
                with ec2:
                    stc.html(_preview_html(comp_json), height=150)

            st.markdown('<hr style="margin:0;border:none;border-top:1px solid #F1F5F9;">', unsafe_allow_html=True)

        if to_delete is not None:
            st.session_state.custom_components.pop(to_delete)
            st.rerun()

    # ── 分 scope 展示现有组件 ──
    def render_scope_section(scope_name, scope_desc, scope_color, scope_bg):
        """渲染一个 scope 分区下的所有组件（列表式 + 调试功能）"""
        scoped = {k: v for k, v in catalog.items() if v["scope"] == scope_name}
        if not scoped:
            return

        count = len(scoped)
        st.markdown(f'''
        <div style="margin:8px 0 4px 0;padding:16px 20px;background:{scope_bg};border-left:3px solid {scope_color};border-radius:0 8px 8px 0;">
            <div style="display:flex;align-items:center;gap:10px;">
                <span style="font-size:16px;font-weight:700;color:#0F172A;">{scope_name}组件</span>
                <span style="font-size:11px;background:{scope_color};color:#fff;padding:2px 10px;border-radius:10px;">{count}</span>
            </div>
            <div style="font-size:12px;color:#64748B;margin-top:4px;">{scope_desc}</div>
        </div>
        ''', unsafe_allow_html=True)

        seen_cats = []
        for v in scoped.values():
            if v["category"] not in seen_cats:
                seen_cats.append(v["category"])

        for cat in seen_cats:
            cat_items = {k: v for k, v in scoped.items() if v["category"] == cat}
            if not cat_items:
                continue

            st.markdown(f'<div style="font-size:13px;font-weight:600;color:#475569;margin:16px 0 8px 4px;">{cat_icons.get(cat, "")} {cat}</div>', unsafe_allow_html=True)

            for comp_name, info in cat_items.items():
                # 如果用户编辑过，用编辑后的 JSON；否则用默认示例
                current_example = st.session_state.edited_examples.get(comp_name, info["example"])

                props_tags = " ".join(
                    f'<span style="display:inline-block;background:#F1F5F9;color:#475569;padding:1px 6px;border-radius:3px;font-size:10px;font-family:monospace;">{k}</span>'
                    for k in info["props"].keys()
                )

                is_edited = comp_name in st.session_state.edited_examples

                col_info, col_preview = st.columns([3, 2], gap="medium")

                with col_info:
                    edited_badge = '<span style="font-size:10px;background:#FEF3C7;color:#D97706;padding:2px 8px;border-radius:10px;margin-left:4px;">已修改</span>' if is_edited else ''
                    st.markdown(f'''
                    <div style="padding:12px 0;">
                        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                            <span style="font-size:14px;font-weight:700;color:#0F172A;font-family:monospace;">{comp_name}</span>
                            <span style="font-size:10px;background:#EEF2FF;color:#4F46E5;padding:2px 8px;border-radius:10px;">{info["category"]}</span>
                            {edited_badge}
                        </div>
                        <div style="font-size:12px;color:#64748B;line-height:1.6;margin-bottom:8px;">{info["description"]}</div>
                        <div style="display:flex;flex-wrap:wrap;gap:4px;align-items:center;">
                            {props_tags}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

                with col_preview:
                    stc.html(_preview_html(current_example), height=90)

                # 调试面板
                with st.expander(f"调试 {comp_name}", expanded=False):
                    dc1, dc2 = st.columns([3, 2], gap="medium")
                    with dc1:
                        edit_val = st.text_input("描述修改", placeholder=f"例如：把标题改成春节活动", key=f"edit_{comp_name}", label_visibility="collapsed")
                        btn_cols = st.columns([1, 1] if is_edited else [1])
                        with btn_cols[0]:
                            if st.button("应用修改", key=f"apply_{comp_name}", use_container_width=True, type="primary") and edit_val:
                                props_desc = ", ".join(f"{k}: {v}" for k, v in info["props"].items())
                                prompt = EDIT_PROMPT.format(comp_type=comp_name, props=props_desc, current_json=json.dumps(current_example, ensure_ascii=False), user_input=edit_val)
                                with st.spinner("修改中..."):
                                    raw = model.generate_with_qwen(edit_val, prompt, API_KEY)
                                    if raw:
                                        try:
                                            st.session_state.edited_examples[comp_name] = _parse_json(raw)
                                            st.rerun()
                                        except:
                                            st.error("修改失败")
                        if is_edited:
                            with btn_cols[1]:
                                if st.button("还原默认", key=f"reset_{comp_name}", use_container_width=True):
                                    del st.session_state.edited_examples[comp_name]
                                    st.rerun()
                        st.code(json.dumps(current_example, ensure_ascii=False, indent=2), language="json")
                    with dc2:
                        stc.html(_preview_html(current_example), height=150)

                st.markdown('<hr style="margin:0;border:none;border-top:1px solid #F1F5F9;">', unsafe_allow_html=True)

    render_scope_section(
        "通用", "可在任何业务场景复用的基础组件，如文本展示、选项选择、按钮操作等",
        "#4F46E5", "#F5F3FF"
    )

    render_scope_section(
        "行业特定", "针对快递物流等垂直场景设计的专用组件，包含地址收集、包裹信息等",
        "#D97706", "#FFFBEB"
    )