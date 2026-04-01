"""
A2UI - 极简界面，高保真预览
"""

import streamlit as st
import streamlit.components.v1 as stc
import json
import model
import components as comp_lib

st.set_page_config(page_title="A2UI", layout="wide", initial_sidebar_state="collapsed")

if 'preview' not in st.session_state:
    st.session_state.preview = ''
if 'json_out' not in st.session_state:
    st.session_state.json_out = ''
if 'query' not in st.session_state:
    st.session_state.query = ''

API_KEY = "Zq2YTTh5DFGtdLpETX1zJ6J8cauCH8Cn"
PROMPT = """你是资深 UI 设计师，根据用户需求生成现代化 UI 组件 JSON。

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

【示例 - 寄快递】
[
  {"type": "StepProgress", "steps": ["下单","取件","运输","签收"], "current": 0},
  {"type": "AddressCollector", "type": "寄件", "name": "", "phone": "", "address": ""},
  {"type": "AddressCollector", "type": "收件", "name": "", "phone": "", "address": ""},
  {"type": "PackageSelector", "options": ["文件", "物品", "生鲜", "数码"]},
  {"type": "Stepper", "label": "包裹重量", "value": 1, "unit": "kg"},
  {"type": "TimePicker", "label": "期望取件时间", "slots": ["09:00-11:00", "14:00-16:00"]},
  {"type": "PriceDetail", "items": [{"label":"基础运费","value":"¥12"},{"label":"包装费","value":"¥3"}], "total": "¥15"},
  {"type": "Notice", "type": "info", "title": "温馨提示", "content": "请确保物品包装完好"},
  {"type": "OrderButton", "label": "确认下单", "price": "¥15"}
]

只输出 JSON 数组，不要其他内容。
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
st.markdown('<div class="app-title">A2UI</div>', unsafe_allow_html=True)

# 左右布局
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
                st.session_state.json_out = json_str.strip()
                try:
                    components = json.loads(st.session_state.json_out)
                    html = comp_lib.render_components(components)
                    st.session_state.preview = comp_lib.wrap_html(html)
                except:
                    st.session_state.preview = '<div>JSON 错误</div>'
        st.rerun()

    if st.session_state.json_out:
        with st.expander("JSON"):
            st.code(st.session_state.json_out, language='json')

with right:
    st.markdown('<div class="section-label">预览</div>', unsafe_allow_html=True)

    if st.session_state.preview:
        # 手机外框
        phone = f'''
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
            ">
                <!-- 灵动岛 -->
                <div style="
                    position: absolute;
                    top: 16px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 90px;
                    height: 26px;
                    background: #000;
                    border-radius: 14px;
                    z-index: 100;
                "></div>
                <!-- 状态栏 -->
                <div style="
                    position: absolute;
                    top: 20px;
                    left: 40px;
                    font-size: 13px;
                    font-weight: 600;
                    color: #000;
                    z-index: 99;
                ">9:41</div>
                <div style="
                    position: absolute;
                    top: 20px;
                    right: 36px;
                    font-size: 12px;
                    z-index: 99;
                ">📶 🔋</div>
                <!-- 内容 -->
                <div style="
                    width: 100%;
                    height: 100%;
                    overflow-y: auto;
                    padding: 54px 10px 36px 10px;
                    box-sizing: border-box;
                    background: #F8F9FA;
                ">
                    {st.session_state.preview}
                </div>
                <!-- Home 条 -->
                <div style="
                    position: absolute;
                    bottom: 6px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 120px;
                    height: 4px;
                    background: #000;
                    border-radius: 2px;
                    opacity: 0.3;
                "></div>
            </div>
        </div>
        '''
        stc.html(phone, height=680)
    else:
        st.markdown("""
        <div style="
            width: 320px;
            height: 600px;
            margin: 0 auto;
            background: #F1F3F4;
            border-radius: 42px;
            border: 2px dashed #CBD5E1;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            color: #94A3B8;
        ">
            <div style="font-size: 40px; opacity: 0.4; margin-bottom: 12px;">📱</div>
            <div style="font-size: 12px;">输入需求后预览</div>
        </div>
        """, unsafe_allow_html=True)