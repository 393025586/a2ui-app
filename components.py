"""
A2UI 组件渲染器 — iOS HIG 风格
基于 Apple Human Interface Guidelines 设计规范
"""

import re

# ══════════════════════════════════════════════════════════════════════════════
# iOS Design Tokens — Tailwind CDN 配置 & 基础样式
# ══════════════════════════════════════════════════════════════════════════════

IOS_TAILWIND_CONFIG = """<script>
tailwind.config = {
    theme: {
        extend: {
            colors: {
                ios: {
                    blue: '#007AFF',
                    green: '#34C759',
                    orange: '#FF9500',
                    red: '#FF3B30',
                    label: '#000000',
                    'label-2': '#8E8E93',
                    'label-3': '#C7C7CC',
                    separator: '#C6C6C8',
                    'bg-2': '#F2F2F7',
                    fill: '#E5E5EA',
                }
            },
            borderRadius: {
                ios: '10px',
                'ios-sm': '8px',
            },
            boxShadow: {
                ios: '0 1px 3px rgba(0,0,0,0.08)',
            },
        }
    }
}
</script>"""

IOS_BASE_STYLES = """<style>
* { font-family: -apple-system, "SF Pro Text", "SF Pro Display", system-ui, sans-serif; }
body { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
</style>"""

# ══════════════════════════════════════════════════════════════════════════════
# 展示类组件
# ══════════════════════════════════════════════════════════════════════════════

def render_heading(comp):
    """标题"""
    text = comp.get("text", "")
    return f'<h2 class="text-[17px] leading-[22px] font-semibold text-ios-label mb-3">{text}</h2>'

def render_paragraph(comp):
    """段落文本"""
    text = comp.get("text", "")
    return f'<p class="text-[15px] leading-[20px] text-ios-label-2 mb-3">{text}</p>'

def render_bullet_list(comp):
    """列表"""
    items = comp.get("items", [])
    html = '<ul class="text-[15px] leading-[20px] text-ios-label-2 mb-3 space-y-2">'
    for item in items:
        html += f'<li class="pl-4 relative before:content-["•"] before:absolute before:left-0">{item}</li>'
    html += '</ul>'
    return html

def render_service_card(comp):
    """服务卡片"""
    title = comp.get("title", "")
    subtitle = comp.get("subtitle", "")
    tag = comp.get("tag", "")
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3">
        <div class="font-semibold text-[17px] leading-[22px] text-ios-label">{title} {f'<span class="text-[12px] leading-[16px] text-ios-blue ml-1">[{tag}]</span>' if tag else ''}</div>
        {f'<div class="text-[13px] leading-[18px] text-ios-label-2 mt-1">{subtitle}</div>' if subtitle else ''}
    </div>
    '''

def render_info_table(comp):
    """信息表格"""
    headers = comp.get("headers", [])
    rows = comp.get("rows", [])
    html = '<div class="bg-white rounded-ios shadow-ios mb-3 overflow-hidden"><table class="w-full">'
    html += '<tr class="border-b border-ios-separator">'
    for h in headers:
        html += f'<th class="px-4 py-3 text-left text-[13px] leading-[18px] text-ios-label-2 font-normal">{h}</th>'
    html += '</tr>'
    for row in rows:
        html += '<tr class="border-b border-ios-separator/30">'
        for key in ["name", "rate", "feature"]:
            if key in row:
                html += f'<td class="px-4 py-3 text-[15px] leading-[20px] text-ios-label">{row[key]}</td>'
        html += '</tr>'
    html += '</table></div>'
    return html

def render_address_item(comp):
    """地址项"""
    type_label = comp.get("type", "寄件")
    name = comp.get("name", "")
    phone = comp.get("phone", "")
    address = comp.get("address", "")
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3">
        <div class="text-[12px] leading-[16px] font-medium text-ios-label-2 mb-2">{type_label}</div>
        <div class="text-[17px] leading-[22px] text-ios-label">{name} {phone}</div>
        <div class="text-[13px] leading-[18px] text-ios-label-2 mt-1">{address}</div>
    </div>
    '''

def render_package_info(comp):
    """包裹信息"""
    weight = comp.get("weight", "")
    type_ = comp.get("type", "")
    value = comp.get("value", "")
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3 flex justify-between text-[15px] leading-[20px]">
        <div><span class="text-ios-label-2">重量:</span> <span class="text-ios-label">{weight}</span></div>
        <div><span class="text-ios-label-2">类型:</span> <span class="text-ios-label">{type_}</span></div>
        <div><span class="text-ios-label-2">保价:</span> <span class="text-ios-label">{value}</span></div>
    </div>
    '''

def render_price_card(comp):
    """价格卡片"""
    items = comp.get("items", [])
    total = comp.get("total", "¥0")
    html = '<div class="bg-white rounded-ios shadow-ios p-4 mb-3"><div class="text-[13px] leading-[18px] font-semibold text-ios-label-2 mb-3">费用明细</div>'
    for item in items:
        html += f'<div class="flex justify-between text-[15px] leading-[20px] mb-2"><span class="text-ios-label-2">{item.get("label","")}</span><span class="text-ios-label">{item.get("value","")}</span></div>'
    html += f'<div class="flex justify-between text-[15px] leading-[20px] pt-3 border-t border-ios-separator mt-3"><span class="font-semibold text-ios-label">合计</span><span class="font-bold text-ios-orange">{total}</span></div></div>'
    return html

def render_timeline(comp):
    """时间线"""
    steps = comp.get("steps", [])
    html = '<div class="bg-white rounded-ios shadow-ios p-4 mb-3">'
    for i, step in enumerate(steps):
        status = step.get("status", "pending")
        time = step.get("time", "")
        desc = step.get("desc", "")
        dot = "●" if status == "completed" else "◉" if status == "current" else "○"
        color = "text-ios-green" if status == "completed" else "text-ios-blue" if status == "current" else "text-ios-label-3"
        html += f'<div class="flex gap-3 text-[15px] leading-[20px] mb-2"><span class="{color}">{dot}</span><span class="text-ios-label-2 shrink-0">{time}</span><span class="text-ios-label">{desc}</span></div>'
    html += '</div>'
    return html

def render_action_button(comp):
    """操作按钮组"""
    actions = comp.get("actions", [])
    html = '<div class="flex gap-3 mb-3">'
    for action in actions:
        label = action.get("label", "操作")
        type_ = action.get("type", "primary")
        if type_ == "primary":
            html += f'<button class="flex-1 bg-ios-blue text-white py-3 text-[17px] leading-[22px] font-semibold rounded-ios min-h-[44px]">{label}</button>'
        else:
            html += f'<button class="flex-1 border border-ios-separator text-ios-label py-3 text-[17px] leading-[22px] rounded-ios min-h-[44px]">{label}</button>'
    html += '</div>'
    return html

def render_notice(comp):
    """提示"""
    type_ = comp.get("type", "info")
    title = comp.get("title", "")
    content = comp.get("content", "")
    colors = {
        "info": "bg-blue-50 border-l-[3px] border-ios-blue",
        "warning": "bg-orange-50 border-l-[3px] border-ios-orange",
        "success": "bg-green-50 border-l-[3px] border-ios-green",
    }
    bg = colors.get(type_, colors["info"])
    return f'''
    <div class="{bg} rounded-ios p-4 mb-3">
        {f'<div class="font-semibold text-[17px] leading-[22px] text-ios-label mb-1">{title}</div>' if title else ''}
        <div class="text-[15px] leading-[20px] text-ios-label-2">{content}</div>
    </div>
    '''

def render_section_header(comp):
    """分组标题"""
    title = comp.get("title", "")
    subtitle = comp.get("subtitle", "")
    return f'''
    <div class="border-l-[3px] border-ios-blue pl-3 mb-3">
        <div class="text-[17px] leading-[22px] font-semibold text-ios-label">{title}</div>
        {f'<div class="text-[13px] leading-[18px] text-ios-label-2">{subtitle}</div>' if subtitle else ''}
    </div>
    '''

def render_step_progress(comp):
    """步骤进度"""
    steps = comp.get("steps", [])
    current = comp.get("current", 0)
    html = '<div class="bg-white rounded-ios shadow-ios p-4 mb-3">'
    for i, step in enumerate(steps):
        status = "completed" if i < current else "current" if i == current else "pending"
        dot = "●" if status == "completed" else "◉" if status == "current" else "○"
        color = "text-ios-green" if status == "completed" else "text-ios-blue" if status == "current" else "text-ios-label-3"
        text_color = "text-ios-label-3" if status == "pending" else "text-ios-label"
        html += f'<div class="flex gap-3 text-[13px] leading-[18px] mb-2"><span class="{color}">{dot}</span><span class="{text_color}">{step}</span></div>'
    html += '</div>'
    return html

def render_address_input(comp):
    """地址输入"""
    label = comp.get("label", "")
    placeholder = comp.get("placeholder", "")
    value = comp.get("value", "")
    text_cls = "text-ios-label" if value else "text-ios-label-3"
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3">
        {f'<div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-2">{label}</div>' if label else ''}
        <div class="bg-ios-bg-2 rounded-ios-sm p-3 text-[15px] leading-[20px] {text_cls}">{value if value else placeholder}</div>
    </div>
    '''

def render_contact_input(comp):
    """联系人输入"""
    label = comp.get("label", "联系人")
    name = comp.get("name", "")
    phone = comp.get("phone", "")
    name_cls = "text-ios-label" if name else "text-ios-label-3"
    phone_cls = "text-ios-label" if phone else "text-ios-label-3"
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3">
        <div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-2">{label}</div>
        <div class="text-[15px] leading-[20px]"><span class="{name_cls}">{name or "姓名"}</span> <span class="text-ios-separator">|</span> <span class="{phone_cls}">{phone or "电话"}</span></div>
    </div>
    '''

def render_package_selector(comp):
    """包裹类型选择"""
    options = comp.get("options", [])
    selected = comp.get("selected", 0)
    html = '<div class="bg-white rounded-ios shadow-ios p-4 mb-3"><div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-3">包裹类型</div><div class="flex flex-wrap gap-2">'
    for i, opt in enumerate(options):
        if i == selected:
            html += f'<span class="bg-ios-blue text-white px-4 py-2 rounded-full text-[15px] leading-[20px]">{opt}</span>'
        else:
            html += f'<span class="bg-ios-fill text-ios-label px-4 py-2 rounded-full text-[15px] leading-[20px]">{opt}</span>'
    html += '</div></div>'
    return html

def render_weight_selector(comp):
    """重量选择器"""
    label = comp.get("label", "包裹重量")
    value = comp.get("value", "1")
    unit = comp.get("unit", "kg")
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3 flex justify-between items-center min-h-[44px]">
        <span class="text-[15px] leading-[20px] text-ios-label-2">{label}</span>
        <span class="text-[17px] leading-[22px] font-semibold text-ios-label">{value}{unit}</span>
    </div>
    '''

def render_time_picker(comp):
    """时间选择器"""
    label = comp.get("label", "期望时间")
    slots = comp.get("slots", [])
    selected = comp.get("selected", 0)
    html = f'<div class="bg-white rounded-ios shadow-ios p-4 mb-3"><div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-3">{label}</div>'
    for i, slot in enumerate(slots):
        if i == selected:
            html += f'<div class="bg-ios-blue text-white px-4 py-3 rounded-ios text-[15px] leading-[20px] mb-2">{slot}</div>'
        else:
            html += f'<div class="bg-ios-bg-2 text-ios-label px-4 py-3 rounded-ios text-[15px] leading-[20px] mb-2">{slot}</div>'
    html += '</div>'
    return html

def render_price_detail(comp):
    """价格明细"""
    items = comp.get("items", [])
    total = comp.get("total", "¥0")
    html = '<div class="bg-white rounded-ios shadow-ios p-4 mb-3"><div class="text-[13px] leading-[18px] font-semibold text-ios-label-2 mb-3">费用明细</div>'
    for item in items:
        html += f'<div class="flex justify-between text-[15px] leading-[20px] mb-2"><span class="text-ios-label-2">{item.get("label","")}</span><span class="text-ios-label">{item.get("value","")}</span></div>'
    html += f'<div class="flex justify-between text-[15px] leading-[20px] pt-3 border-t border-ios-separator mt-3"><span class="font-semibold text-ios-label">合计</span><span class="font-bold text-ios-orange">{total}</span></div></div>'
    return html

def render_coupon(comp):
    """优惠券"""
    title = comp.get("title", "")
    amount = comp.get("amount", "")
    condition = comp.get("condition", "")
    return f'''
    <div class="bg-orange-50 border border-ios-orange/20 rounded-ios shadow-ios p-4 mb-3 flex justify-between items-center">
        <div>
            <div class="text-[17px] leading-[22px] font-semibold text-ios-label">{title}</div>
            {f'<div class="text-[13px] leading-[18px] text-ios-orange mt-1">{condition}</div>' if condition else ''}
        </div>
        <div class="text-2xl font-bold text-ios-orange">{amount}</div>
    </div>
    '''

def render_submit_button(comp):
    """提交按钮"""
    label = comp.get("label", "提交")
    price = comp.get("price", "")
    return f'<button class="w-full bg-ios-blue text-white py-3 text-[17px] leading-[22px] font-semibold rounded-ios min-h-[44px] mb-3">{label} {price}</button>'

# ==============================================================================
# 意图澄清组件
# ==============================================================================

def render_tag_options(comp):
    """标签选项"""
    label = comp.get("label", "")
    options = comp.get("options", [])
    selected = comp.get("selected", None)
    html = f'<div class="bg-white rounded-ios shadow-ios p-4 mb-3">'
    html += f'<div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-3">{label}</div>' if label else ''
    html += '<div class="flex flex-wrap gap-2">'
    for opt in options:
        is_selected = (isinstance(selected, list) and opt in selected) or opt == selected
        if is_selected:
            html += f'<span class="bg-ios-blue text-white px-4 py-2 rounded-full text-[15px] leading-[20px]">{opt}</span>'
        else:
            html += f'<span class="bg-ios-fill text-ios-label px-4 py-2 rounded-full text-[15px] leading-[20px]">{opt}</span>'
    html += '</div></div>'
    return html

def render_amount_option(comp):
    """金额选项"""
    label = comp.get("label", "选择金额")
    options = comp.get("options", [])
    selected = comp.get("selected", 0)
    html = f'<div class="bg-white rounded-ios shadow-ios p-4 mb-3"><div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-3">{label}</div><div class="flex flex-wrap gap-2">'
    for i, opt in enumerate(options):
        if i == selected:
            html += f'<span class="bg-ios-blue text-white px-4 py-2 rounded-full text-[15px] leading-[20px]">{opt}</span>'
        else:
            html += f'<span class="bg-ios-fill text-ios-label px-4 py-2 rounded-full text-[15px] leading-[20px]">{opt}</span>'
    html += '</div></div>'
    return html

def render_list_option(comp):
    """列表选项"""
    label = comp.get("label", "")
    options = comp.get("options", [])
    selected = comp.get("selected", None)
    html = f'<div class="bg-white rounded-ios shadow-ios p-4 mb-3">'
    html += f'<div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-3">{label}</div>' if label else ''
    for i, opt in enumerate(options):
        title = opt.get("title", "")
        subtitle = opt.get("subtitle", "")
        is_selected = i == selected
        border = "border-ios-blue bg-blue-50" if is_selected else "border-ios-separator/50"
        check = "●" if is_selected else "○"
        html += f'''
        <div class="border {border} rounded-ios p-3 mb-2 flex justify-between items-center min-h-[44px]">
            <div>
                <div class="text-[15px] leading-[20px] text-ios-label">{title}</div>
                {f'<div class="text-[13px] leading-[18px] text-ios-label-2">{subtitle}</div>' if subtitle else ''}
            </div>
            <span class="text-ios-blue text-[16px]">{check}</span>
        </div>
        '''
    html += '</div>'
    return html

def render_stepper(comp):
    """步进器"""
    label = comp.get("label", "")
    value = comp.get("value", 1)
    unit = comp.get("unit", "")
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3 flex justify-between items-center min-h-[44px]">
        <span class="text-[15px] leading-[20px] text-ios-label-2">{label}</span>
        <div class="flex items-center gap-3">
            <span class="w-8 h-8 bg-ios-fill rounded-full text-center leading-8 text-[17px] text-ios-label">−</span>
            <span class="text-[17px] leading-[22px] font-semibold text-ios-label">{value}</span>
            <span class="w-8 h-8 bg-ios-blue text-white rounded-full text-center leading-8 text-[17px]">+</span>
        </div>
        {f'<span class="text-[13px] leading-[18px] text-ios-label-2">{unit}</span>' if unit else ''}
    </div>
    '''

def render_text_input(comp):
    """单行文本输入"""
    label = comp.get("label", "")
    placeholder = comp.get("placeholder", "请输入")
    value = comp.get("value", "")
    text_cls = "text-ios-label" if value else "text-ios-label-3"
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3">
        {f'<div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-2">{label}</div>' if label else ''}
        <div class="bg-ios-bg-2 rounded-ios-sm p-3 text-[15px] leading-[20px] {text_cls}">{value if value else placeholder}</div>
    </div>
    '''

def render_textarea_input(comp):
    """多行文本输入"""
    label = comp.get("label", "")
    placeholder = comp.get("placeholder", "请输入内容")
    value = comp.get("value", "")
    text_cls = "text-ios-label" if value else "text-ios-label-3"
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3">
        {f'<div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-2">{label}</div>' if label else ''}
        <div class="bg-ios-bg-2 rounded-ios-sm p-3 text-[15px] leading-[20px] {text_cls} min-h-[80px]">{value if value else placeholder}</div>
    </div>
    '''

def render_phone_input(comp):
    """手机号码输入"""
    label = comp.get("label", "手机号码")
    placeholder = comp.get("placeholder", "请输入手机号")
    value = comp.get("value", "")
    text_cls = "text-ios-label" if value else "text-ios-label-3"
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3">
        {f'<div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-2">{label}</div>' if label else ''}
        <div class="bg-ios-bg-2 rounded-ios-sm p-3 text-[15px] leading-[20px] {text_cls}">{value if value else placeholder}</div>
    </div>
    '''

def render_amount_input(comp):
    """金额输入"""
    label = comp.get("label", "金额")
    placeholder = comp.get("placeholder", "0.00")
    value = comp.get("value", "")
    text_cls = "text-ios-label" if value else "text-ios-label-3"
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3">
        {f'<div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-2">{label}</div>' if label else ''}
        <div class="bg-ios-bg-2 rounded-ios-sm p-3 text-[15px] leading-[20px] {text_cls}">¥ {value if value else placeholder}</div>
    </div>
    '''

def render_confirm_button(comp):
    """确认按钮"""
    label = comp.get("label", "确认")
    disabled = comp.get("disabled", False)
    bg = "bg-ios-fill text-ios-label-3" if disabled else "bg-ios-blue text-white"
    return f'<button class="w-full {bg} py-3 text-[17px] leading-[22px] font-semibold rounded-ios min-h-[44px] mb-3">{label}</button>'

def render_text_link(comp):
    """文字链接"""
    text = comp.get("text", "查看详情")
    href = comp.get("href", "#")
    return f'<a href="{href}" class="text-[15px] leading-[20px] text-ios-blue mb-3 block">{text}</a>'

def render_order_button(comp):
    """下单按钮"""
    label = comp.get("label", "立即下单")
    price = comp.get("price", "¥0")
    disabled = comp.get("disabled", False)
    bg = "bg-ios-fill text-ios-label-3" if disabled else "bg-ios-blue text-white"
    return f'<button class="w-full {bg} py-3 text-[17px] leading-[22px] font-semibold rounded-ios min-h-[44px] mb-3">{label} · {price}</button>'

def render_address_collector(comp):
    """收/寄件地址收集"""
    type_ = comp.get("type", "寄件")
    name = comp.get("name", "")
    phone = comp.get("phone", "")
    address = comp.get("address", "")
    name_cls = "text-ios-label" if name else "text-ios-label-3"
    phone_cls = "text-ios-label" if phone else "text-ios-label-3"
    addr_cls = "text-ios-label" if address else "text-ios-label-3"
    return f'''
    <div class="bg-white rounded-ios shadow-ios p-4 mb-3">
        <div class="text-[13px] leading-[18px] font-medium text-ios-label-2 mb-3">{type_}地址</div>
        <div class="space-y-2">
            <div class="bg-ios-bg-2 rounded-ios-sm p-3 text-[15px] leading-[20px] {name_cls}">{name or "姓名"}</div>
            <div class="bg-ios-bg-2 rounded-ios-sm p-3 text-[15px] leading-[20px] {phone_cls}">{phone or "手机号"}</div>
            <div class="bg-ios-bg-2 rounded-ios-sm p-3 text-[15px] leading-[20px] {addr_cls}">{address or "详细地址"}</div>
        </div>
    </div>
    '''

def render_auth_button(comp):
    """授权按钮"""
    label = comp.get("label", "同意并授权")
    agreement = comp.get("agreement", "《用户协议》")
    checked = comp.get("checked", False)
    check = "☑" if checked else "☐"
    return f'''
    <div class="mb-3">
        <div class="flex items-center gap-2 mb-3 text-[15px] leading-[20px] text-ios-label-2">
            <span class="text-ios-blue">{check}</span>
            <span>同意{agreement}</span>
        </div>
        <button class="w-full bg-ios-blue text-white py-3 text-[17px] leading-[22px] font-semibold rounded-ios min-h-[44px]">{label}</button>
    </div>
    '''

def render_verify_button(comp):
    """核身按钮"""
    label = comp.get("label", "实名认证")
    agreement = comp.get("agreement", "《隐私协议》")
    checked = comp.get("checked", False)
    id_number = comp.get("idNumber", "")
    check = "☑" if checked else "☐"
    id_cls = "text-ios-label" if id_number else "text-ios-label-3"
    return f'''
    <div class="mb-3">
        <div class="flex items-center gap-2 mb-3 text-[15px] leading-[20px] text-ios-label-2">
            <span class="text-ios-blue">{check}</span>
            <span>同意{agreement}</span>
        </div>
        {f'<div class="bg-ios-bg-2 rounded-ios-sm p-3 text-[15px] leading-[20px] {id_cls} mb-3">{id_number or "身份证号"}</div>' if id_number is not None else ''}
        <button class="w-full bg-ios-blue text-white py-3 text-[17px] leading-[22px] font-semibold rounded-ios min-h-[44px]">{label}</button>
    </div>
    '''

def render_pay_button(comp):
    """支付按钮"""
    label = comp.get("label", "立即支付")
    amount = comp.get("amount", "¥0")
    disabled = comp.get("disabled", False)
    bg = "bg-ios-fill text-ios-label-3" if disabled else "bg-ios-blue text-white"
    return f'<button class="w-full {bg} py-3 text-[17px] leading-[22px] font-semibold rounded-ios min-h-[44px] mb-3">{label} · {amount}</button>'

# ==============================================================================
# 渲染器映射
# ==============================================================================

RENDERERS = {
    "Heading": render_heading,
    "Paragraph": render_paragraph,
    "BulletList": render_bullet_list,
    "ServiceCard": render_service_card,
    "InfoTable": render_info_table,
    "Notice": render_notice,
    "SectionHeader": render_section_header,
    "Timeline": render_timeline,
    "StepProgress": render_step_progress,
    "AddressItem": render_address_item,
    "PackageInfo": render_package_info,
    "PriceCard": render_price_card,
    "PriceDetail": render_price_detail,
    "Coupon": render_coupon,
    "AddressInput": render_address_input,
    "ContactInput": render_contact_input,
    "PackageSelector": render_package_selector,
    "WeightSelector": render_weight_selector,
    "TimePicker": render_time_picker,
    "ActionButton": render_action_button,
    "SubmitButton": render_submit_button,
    "TagOptions": render_tag_options,
    "AmountOption": render_amount_option,
    "ListOption": render_list_option,
    "Stepper": render_stepper,
    "TextInput": render_text_input,
    "TextareaInput": render_textarea_input,
    "PhoneInput": render_phone_input,
    "AmountInput": render_amount_input,
    "ConfirmButton": render_confirm_button,
    "TextLink": render_text_link,
    "OrderButton": render_order_button,
    "AddressCollector": render_address_collector,
    "AuthButton": render_auth_button,
    "VerifyButton": render_verify_button,
    "PayButton": render_pay_button,
}

def render_component(comp):
    if not isinstance(comp, dict):
        return str(comp)
    comp_type = comp.get("type") or comp.get("component", "")
    if "props" in comp:
        comp = {**comp, **comp["props"]}
    renderer = RENDERERS.get(comp_type)
    if not renderer:
        return f'<div class="border border-dashed border-ios-separator rounded-ios p-3 text-[13px] leading-[18px] text-ios-label-3 mb-3">[{comp_type}]</div>'
    try:
        return renderer(comp)
    except Exception as e:
        return f'<div class="border border-ios-red/20 bg-red-50 rounded-ios p-3 text-[13px] leading-[18px] text-ios-red mb-3">error: {comp_type}</div>'

def render_components(components):
    if not components:
        return ""
    if isinstance(components, str):
        return components
    if not isinstance(components, list):
        components = [components]
    return "".join(render_component(c) for c in components)

def wrap_html(content, user_query=""):
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    {IOS_TAILWIND_CONFIG}
    {IOS_BASE_STYLES}
</head>
<body class="bg-ios-bg-2 p-4">
    {content}
</body>
</html>'''

def simple_markdown(text):
    """将简单 markdown 转为 HTML"""
    if not text:
        return ""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    lines = text.split('\n')
    result = []
    in_list = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                result.append('<ul style="margin:8px 0;padding-left:20px;">')
                in_list = True
            item = stripped[2:]
            result.append(f'<li style="margin:4px 0;color:#000;font-size:17px;line-height:1.4;">{item}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if stripped:
                result.append(f'<p style="margin:8px 0;color:#000;font-size:17px;line-height:1.4;">{stripped}</p>')
    if in_list:
        result.append('</ul>')
    return '\n'.join(result)

def render_chat_html(user_query, agent_text="", component_html=""):
    """渲染对话气泡 HTML 片段（不含 html/body 包装）"""
    md_html = simple_markdown(agent_text)

    agent_text_block = f'''
        <div style="font-size:17px;line-height:1.4;color:#000;">
            {md_html}
        </div>
    ''' if md_html else ""

    component_block = f'''
        <div style="margin-top:{'8' if md_html else '0'}px;">
            {component_html}
        </div>
    ''' if component_html else ""

    return f'''
    <div style="padding:16px 12px 20px 12px;">
        <!-- 用户消息 -->
        <div style="display:flex;justify-content:flex-end;margin-bottom:16px;">
            <div style="
                max-width:75%;
                background:#007AFF;
                color:#fff;
                padding:10px 16px;
                border-radius:18px;
                font-size:17px;
                line-height:1.4;
                word-break:break-word;
                position:relative;
            ">
                <div style="
                    position:absolute;
                    top:12px;right:-6px;
                    width:0;height:0;
                    border-top:6px solid transparent;
                    border-bottom:6px solid transparent;
                    border-left:6px solid #007AFF;
                "></div>
                {user_query}
            </div>
            <div style="
                width:36px;height:36px;
                background:linear-gradient(135deg,#5AC8FA,#007AFF);
                border-radius:50%;
                margin-left:8px;
                flex-shrink:0;
                display:flex;align-items:center;justify-content:center;
                font-size:14px;color:#fff;font-weight:600;
            ">Me</div>
        </div>

        <!-- Agent 回复 -->
        <div style="display:flex;align-items:flex-start;margin-bottom:16px;">
            <div style="
                width:36px;height:36px;
                background:linear-gradient(135deg,#5856D6,#AF52DE);
                border-radius:50%;
                margin-right:8px;
                flex-shrink:0;
                display:flex;align-items:center;justify-content:center;
                font-size:14px;color:#fff;
            ">AI</div>
            <div style="max-width:80%;position:relative;">
                <div style="
                    position:absolute;
                    top:12px;left:-6px;
                    width:0;height:0;
                    border-top:6px solid transparent;
                    border-bottom:6px solid transparent;
                    border-right:6px solid #fff;
                "></div>
                <div style="
                    background:#fff;
                    border-radius:18px;
                    padding:12px 16px;
                    word-break:break-word;
                ">
                    {agent_text_block}
                    {component_block}
                </div>
            </div>
        </div>
    </div>
    '''

# ==============================================================================
# 组件元数据目录 — 用于组件库展示
# ==============================================================================

COMPONENT_CATALOG = {
    # ── 展示类 ──────────────────────────────────────────────
    "Heading": {
        "scope": "通用",
        "category": "展示类",
        "description": "页面标题组件，用于在内容顶部显示一级标题。适合作为一个回复卡片的开头，概括当前内容主题。",
        "props": {"text": "标题文字"},
        "example": {"type": "Heading", "text": "快递寄送服务"},
    },
    "Paragraph": {
        "scope": "通用",
        "category": "展示类",
        "description": "正文段落组件，用于展示一段说明性文字。适合对服务、规则、注意事项进行简要文字描述，常跟在标题之后。",
        "props": {"text": "段落内容"},
        "example": {"type": "Paragraph", "text": "我们提供同城/跨城快递服务，预计 1-3 天送达，支持上门取件。"},
    },
    "InfoTable": {
        "scope": "通用",
        "category": "展示类",
        "description": "信息表格组件，以表格形式展示结构化数据。适合对比多项信息，如基金列表、费率对比、套餐方案等。",
        "props": {"headers": "表头数组", "rows": "行数据数组，每行为 {name, rate, feature} 对象"},
        "example": {"type": "InfoTable", "headers": ["产品", "费率", "特点"], "rows": [{"name": "余额宝", "rate": "2.1%", "feature": "随存随取"}, {"name": "定期理财", "rate": "3.5%", "feature": "封闭 30 天"}]},
    },
    "PriceCard": {
        "scope": "通用",
        "category": "展示类",
        "description": "价格卡片组件，带「费用明细」标题的价格分项列表，底部显示合计。适合展示订单费用构成，如运费、包装费、保价费等。",
        "props": {"items": "费用项数组 [{label, value}]", "total": "合计金额"},
        "example": {"type": "PriceCard", "items": [{"label": "基础运费", "value": "¥12"}, {"label": "包装费", "value": "¥3"}, {"label": "保价费", "value": "¥2"}], "total": "¥17"},
    },

    # ── 输入/选择类 ────────────────────────────────────────
    "AddressInput": {
        "scope": "行业特定",
        "category": "输入选择类",
        "description": "地址输入组件，提供一个地址文本输入区域。用户可手动填写或从地址簿选择。适合需要用户提供地址的场景，如寄件地址、收货地址等。",
        "props": {"label": "输入框标签", "placeholder": "占位提示文字", "value": "预填值（可选）"},
        "example": {"type": "AddressInput", "label": "收货地址", "placeholder": "请输入详细地址", "value": ""},
    },
    "ContactInput": {
        "scope": "行业特定",
        "category": "输入选择类",
        "description": "联系人输入组件，包含姓名和电话两个字段。适合在寄件、预约等场景收集联系人信息。",
        "props": {"label": "标签", "name": "姓名预填值", "phone": "电话预填值"},
        "example": {"type": "ContactInput", "label": "寄件人", "name": "", "phone": ""},
    },
    "TagOptions": {
        "scope": "通用",
        "category": "输入选择类",
        "description": "标签选项组件，以可换行的标签按钮组让用户选择一个或多个选项。这是最通用的意图澄清组件，适合场景分类、偏好选择、功能入口等多选/单选场景。",
        "props": {"label": "标签说明", "options": "选项数组", "selected": "已选中的值（字符串或数组）"},
        "example": {"type": "TagOptions", "label": "你想办理哪项业务？", "options": ["话费充值", "流量包", "宽带续费", "账单查询"], "selected": "话费充值"},
    },
    "AmountOption": {
        "scope": "通用",
        "category": "输入选择类",
        "description": "金额选项组件，以横向标签展示预设金额选项。适合话费充值、红包金额、转账金额等需要从固定金额中选择的场景。",
        "props": {"label": "标签", "options": "金额选项数组", "selected": "默认选中索引"},
        "example": {"type": "AmountOption", "label": "充值金额", "options": ["¥30", "¥50", "¥100", "¥200"], "selected": 2},
    },
    "ListOption": {
        "scope": "通用",
        "category": "输入选择类",
        "description": "列表选项组件，每个选项为带标题和副标题的卡片，右侧有单选圆点。适合在多个方案/服务中选择一项，如快递公司选择、保险方案选择等。",
        "props": {"label": "标签", "options": "选项数组 [{title, subtitle}]", "selected": "选中索引"},
        "example": {"type": "ListOption", "label": "选择快递公司", "options": [{"title": "顺丰速运", "subtitle": "预计明天送达 · ¥23"}, {"title": "中通快递", "subtitle": "预计后天送达 · ¥12"}, {"title": "韵达快递", "subtitle": "预计后天送达 · ¥10"}], "selected": 0},
    },
    "Stepper": {
        "scope": "通用",
        "category": "输入选择类",
        "description": "步进器组件，带 +/- 按钮的数值调节器。适合调整数量、重量、份数等数值型输入，用户可通过按钮快速增减。",
        "props": {"label": "标签", "value": "当前值", "unit": "单位（可选）"},
        "example": {"type": "Stepper", "label": "购买数量", "value": 2, "unit": "份"},
    },
    "TextInput": {
        "scope": "通用",
        "category": "输入选择类",
        "description": "单行文本输入组件，提供一个简单的文本输入框。适合收集短文本信息，如姓名、快递单号、验证码等。",
        "props": {"label": "标签", "placeholder": "占位提示", "value": "预填值"},
        "example": {"type": "TextInput", "label": "快递单号", "placeholder": "请输入运单号", "value": ""},
    },
    "TextareaInput": {
        "scope": "通用",
        "category": "输入选择类",
        "description": "多行文本输入组件，提供一个可输入多行文字的区域。适合收集备注、留言、问题描述等较长文本。",
        "props": {"label": "标签", "placeholder": "占位提示", "value": "预填值"},
        "example": {"type": "TextareaInput", "label": "备注信息", "placeholder": "如有特殊要求请在此说明", "value": ""},
    },
    "PhoneInput": {
        "scope": "通用",
        "category": "输入选择类",
        "description": "手机号码输入组件，专用于手机号收集。适合注册、验证身份、联系人信息填写等需要手机号的场景。",
        "props": {"label": "标签", "placeholder": "占位提示", "value": "预填值"},
        "example": {"type": "PhoneInput", "label": "手机号码", "placeholder": "请输入 11 位手机号", "value": ""},
    },
    "AmountInput": {
        "scope": "通用",
        "category": "输入选择类",
        "description": "金额输入组件，带 ¥ 前缀的金额输入框。适合自定义转账金额、充值金额、还款金额等需要用户手动输入金额的场景。",
        "props": {"label": "标签", "placeholder": "占位提示", "value": "预填值"},
        "example": {"type": "AmountInput", "label": "转账金额", "placeholder": "0.00", "value": ""},
    },

    # ── 按钮类 ──────────────────────────────────────────────
    "ActionButton": {
        "scope": "通用",
        "category": "按钮类",
        "description": "操作按钮组组件，可在一行内放置多个按钮（主要/次要）。适合同时提供「确认」和「取消」等多个并列操作选项。",
        "props": {"actions": "按钮数组 [{label, type}]，type 可选 primary/secondary"},
        "example": {"type": "ActionButton", "actions": [{"label": "取消", "type": "secondary"}, {"label": "确认提交", "type": "primary"}]},
    },
    "ConfirmButton": {
        "scope": "通用",
        "category": "按钮类",
        "description": "确认按钮组件，全宽蓝色主按钮。最基础的操作按钮，适合表单提交、流程确认等单一操作。可通过 disabled 控制是否可点击。",
        "props": {"label": "按钮文字", "disabled": "是否禁用（布尔值）"},
        "example": {"type": "ConfirmButton", "label": "确认提交"},
    },
    "TextLink": {
        "scope": "通用",
        "category": "按钮类",
        "description": "文字链接组件，以蓝色文字链接形式展示。适合「查看详情」「了解更多」等辅助跳转操作，不占据主视觉焦点。",
        "props": {"text": "链接文字", "href": "跳转地址"},
        "example": {"type": "TextLink", "text": "查看完整服务协议 →", "href": "#"},
    },
    "OrderButton": {
        "scope": "通用",
        "category": "按钮类",
        "description": "下单按钮组件，全宽蓝色按钮，右侧显示价格。适合购物、寄件等需要展示总价的下单确认场景，让用户一目了然地看到操作和费用。",
        "props": {"label": "按钮文字", "price": "显示金额", "disabled": "是否禁用"},
        "example": {"type": "OrderButton", "label": "确认下单", "price": "¥23"},
    },
    "SubmitButton": {
        "scope": "通用",
        "category": "按钮类",
        "description": "提交按钮组件，全宽蓝色按钮，可附带金额显示。适合提交表单、提交申请等场景。",
        "props": {"label": "按钮文字", "price": "金额（可选）"},
        "example": {"type": "SubmitButton", "label": "提交申请", "price": ""},
    },
    "PayButton": {
        "scope": "通用",
        "category": "按钮类",
        "description": "支付按钮组件，全宽蓝色按钮，显示支付金额。适合支付确认页的最终操作按钮，如话费充值确认、订单支付等。",
        "props": {"label": "按钮文字", "amount": "支付金额", "disabled": "是否禁用"},
        "example": {"type": "PayButton", "label": "立即支付", "amount": "¥100"},
    },
    "AuthButton": {
        "scope": "通用",
        "category": "按钮类",
        "description": "授权按钮组件，包含协议勾选框和授权按钮。用户需先勾选同意协议才能操作。适合开通服务、签约代扣等需要用户授权的场景。",
        "props": {"label": "按钮文字", "agreement": "协议名称", "checked": "是否已勾选"},
        "example": {"type": "AuthButton", "label": "同意并开通", "agreement": "《自动续费服务协议》", "checked": False},
    },
    "VerifyButton": {
        "scope": "通用",
        "category": "按钮类",
        "description": "核身验证按钮组件，包含协议勾选、身份证号输入和验证按钮。适合实名认证、身份核验等需要提交身份信息的高安全级别操作。",
        "props": {"label": "按钮文字", "agreement": "协议名称", "checked": "是否已勾选", "idNumber": "身份证号预填值"},
        "example": {"type": "VerifyButton", "label": "实名认证", "agreement": "《隐私保护协议》", "checked": False, "idNumber": ""},
    },

}