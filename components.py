"""
A2UI 组件渲染器 - 简洁草稿版
定位：草稿生成器，注重核心逻辑表达
"""

def render_heading(comp):
    """标题"""
    text = comp.get("text", "")
    return f'<h2 class="text-base font-bold text-slate-900 mb-2">{text}</h2>'

def render_paragraph(comp):
    """段落文本"""
    text = comp.get("text", "")
    return f'<p class="text-sm text-slate-600 mb-2">{text}</p>'

def render_bullet_list(comp):
    """列表"""
    items = comp.get("items", [])
    html = '<ul class="text-sm text-slate-600 mb-2 space-y-1">'
    for item in items:
        html += f'<li class="pl-3 relative before:content-["·"] before:absolute before:left-0">{item}</li>'
    html += '</ul>'
    return html

def render_service_card(comp):
    """服务卡片"""
    title = comp.get("title", "")
    subtitle = comp.get("subtitle", "")
    tag = comp.get("tag", "")
    return f'''
    <div class="border border-slate-200 p-3 mb-2">
        <div class="font-medium text-sm text-slate-900">{title} {f'<span class="text-xs text-blue-600 ml-1">[{tag}]</span>' if tag else ''}</div>
        {f'<div class="text-xs text-slate-500 mt-1">{subtitle}</div>' if subtitle else ''}
    </div>
    '''

def render_info_table(comp):
    """信息表格"""
    headers = comp.get("headers", [])
    rows = comp.get("rows", [])
    html = '<div class="border border-slate-200 mb-2 text-xs"><table class="w-full">'
    html += '<tr class="border-b border-slate-100">'
    for h in headers:
        html += f'<th class="p-2 text-left text-slate-400 font-normal">{h}</th>'
    html += '</tr>'
    for row in rows:
        html += '<tr class="border-b border-slate-50">'
        for key in ["name", "rate", "feature"]:
            if key in row:
                html += f'<td class="p-2 text-slate-700">{row[key]}</td>'
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
    <div class="border border-slate-200 p-3 mb-2">
        <div class="text-xs font-medium text-slate-500 mb-2">{type_label}</div>
        <div class="text-sm text-slate-700">{name} {phone}</div>
        <div class="text-xs text-slate-500 mt-1">{address}</div>
    </div>
    '''

def render_package_info(comp):
    """包裹信息"""
    weight = comp.get("weight", "")
    type_ = comp.get("type", "")
    value = comp.get("value", "")
    return f'''
    <div class="border border-slate-200 p-3 mb-2 flex justify-between text-sm">
        <div><span class="text-slate-400">重量:</span> {weight}</div>
        <div><span class="text-slate-400">类型:</span> {type_}</div>
        <div><span class="text-slate-400">保价:</span> {value}</div>
    </div>
    '''

def render_price_card(comp):
    """价格卡片"""
    items = comp.get("items", [])
    total = comp.get("total", "¥0")
    html = '<div class="border border-slate-200 p-3 mb-2"><div class="text-xs font-medium text-slate-500 mb-2">费用明细</div>'
    for item in items:
        html += f'<div class="flex justify-between text-sm mb-1"><span class="text-slate-600">{item.get("label","")}</span><span>{item.get("value","")}</span></div>'
    html += f'<div class="flex justify-between text-sm pt-2 border-t border-slate-100 mt-2"><span class="font-medium">合计</span><span class="font-bold text-orange-600">{total}</span></div></div>'
    return html

def render_timeline(comp):
    """时间线"""
    steps = comp.get("steps", [])
    html = '<div class="border border-slate-200 p-3 mb-2">'
    for i, step in enumerate(steps):
        status = step.get("status", "pending")
        time = step.get("time", "")
        desc = step.get("desc", "")
        dot = "●" if status == "completed" else "○" if status == "current" else "○"
        color = "text-green-500" if status == "completed" else "text-blue-500" if status == "current" else "text-slate-300"
        html += f'<div class="flex gap-2 text-sm mb-1"><span class="{color}">{dot}</span><span class="text-slate-400">{time}</span><span class="text-slate-700">{desc}</span></div>'
    html += '</div>'
    return html

def render_action_button(comp):
    """操作按钮组"""
    actions = comp.get("actions", [])
    html = '<div class="flex gap-2 mb-2">'
    for action in actions:
        label = action.get("label", "操作")
        type_ = action.get("type", "primary")
        if type_ == "primary":
            html += f'<button class="flex-1 bg-blue-500 text-white py-2 text-sm font-medium">{label}</button>'
        else:
            html += f'<button class="flex-1 border border-slate-300 text-slate-700 py-2 text-sm">{label}</button>'
    html += '</div>'
    return html

def render_notice(comp):
    """提示"""
    type_ = comp.get("type", "info")
    title = comp.get("title", "")
    content = comp.get("content", "")
    bg = "bg-blue-50 border-blue-200" if type_ == "info" else "bg-amber-50 border-amber-200" if type_ == "warning" else "bg-green-50 border-green-200"
    return f'''
    <div class="border {bg} p-3 mb-2 text-sm">
        {f'<div class="font-medium text-slate-700 mb-1">{title}</div>' if title else ''}
        <div class="text-slate-600">{content}</div>
    </div>
    '''

def render_section_header(comp):
    """分组标题"""
    title = comp.get("title", "")
    subtitle = comp.get("subtitle", "")
    return f'''
    <div class="border-l-2 border-slate-300 pl-2 mb-2">
        <div class="text-sm font-bold text-slate-800">{title}</div>
        {f'<div class="text-xs text-slate-400">{subtitle}</div>' if subtitle else ''}
    </div>
    '''

def render_step_progress(comp):
    """步骤进度"""
    steps = comp.get("steps", [])
    current = comp.get("current", 0)
    html = '<div class="border border-slate-200 p-3 mb-2">'
    for i, step in enumerate(steps):
        status = "completed" if i < current else "current" if i == current else "pending"
        dot = "●" if status == "completed" else "○" if status == "current" else "○"
        color = "text-green-500" if status == "completed" else "text-blue-500" if status == "current" else "text-slate-300"
        text_color = "text-slate-400" if status == "pending" else "text-slate-700"
        html += f'<div class="flex gap-2 text-xs mb-1"><span class="{color}">{dot}</span><span class="{text_color}">{step}</span></div>'
    html += '</div>'
    return html

def render_address_input(comp):
    """地址输入"""
    label = comp.get("label", "")
    placeholder = comp.get("placeholder", "")
    value = comp.get("value", "")
    return f'''
    <div class="border border-slate-200 p-3 mb-2">
        {f'<div class="text-xs font-medium text-slate-500 mb-2">{label}</div>' if label else ''}
        <div class="bg-slate-50 p-2 text-sm text-slate-600">{value if value else placeholder}</div>
    </div>
    '''

def render_contact_input(comp):
    """联系人输入"""
    label = comp.get("label", "联系人")
    name = comp.get("name", "")
    phone = comp.get("phone", "")
    return f'''
    <div class="border border-slate-200 p-3 mb-2">
        <div class="text-xs font-medium text-slate-500 mb-2">{label}</div>
        <div class="text-sm text-slate-700">{name or "姓名"} | {phone or "电话"}</div>
    </div>
    '''

def render_package_selector(comp):
    """包裹类型选择"""
    options = comp.get("options", [])
    selected = comp.get("selected", 0)
    html = '<div class="border border-slate-200 p-3 mb-2"><div class="text-xs font-medium text-slate-500 mb-2">包裹类型</div><div class="flex gap-2">'
    for i, opt in enumerate(options):
        if i == selected:
            html += f'<span class="bg-blue-500 text-white px-3 py-1 text-sm">{opt}</span>'
        else:
            html += f'<span class="bg-slate-100 text-slate-600 px-3 py-1 text-sm">{opt}</span>'
    html += '</div></div>'
    return html

def render_weight_selector(comp):
    """重量选择器"""
    label = comp.get("label", "包裹重量")
    value = comp.get("value", "1")
    unit = comp.get("unit", "kg")
    return f'''
    <div class="border border-slate-200 p-3 mb-2 flex justify-between items-center">
        <span class="text-xs font-medium text-slate-500">{label}</span>
        <span class="text-sm font-bold">{value}{unit}</span>
    </div>
    '''

def render_time_picker(comp):
    """时间选择器"""
    label = comp.get("label", "期望时间")
    slots = comp.get("slots", [])
    selected = comp.get("selected", 0)
    html = f'<div class="border border-slate-200 p-3 mb-2"><div class="text-xs font-medium text-slate-500 mb-2">{label}</div>'
    for i, slot in enumerate(slots):
        if i == selected:
            html += f'<div class="bg-blue-500 text-white px-3 py-1 text-sm mb-1">{slot}</div>'
        else:
            html += f'<div class="bg-slate-50 text-slate-600 px-3 py-1 text-sm mb-1">{slot}</div>'
    html += '</div>'
    return html

def render_price_detail(comp):
    """价格明细"""
    items = comp.get("items", [])
    total = comp.get("total", "¥0")
    html = '<div class="border border-slate-200 p-3 mb-2"><div class="text-xs font-medium text-slate-500 mb-2">费用明细</div>'
    for item in items:
        html += f'<div class="flex justify-between text-sm mb-1"><span class="text-slate-600">{item.get("label","")}</span><span>{item.get("value","")}</span></div>'
    html += f'<div class="flex justify-between text-sm pt-2 border-t border-slate-100 mt-2"><span class="font-medium">合计</span><span class="font-bold text-orange-600">{total}</span></div></div>'
    return html

def render_coupon(comp):
    """优惠券"""
    title = comp.get("title", "")
    amount = comp.get("amount", "")
    condition = comp.get("condition", "")
    return f'''
    <div class="border border-orange-200 bg-orange-50 p-3 mb-2 flex justify-between items-center">
        <div>
            <div class="text-sm font-medium text-orange-800">{title}</div>
            {f'<div class="text-xs text-orange-600">{condition}</div>' if condition else ''}
        </div>
        <div class="text-lg font-bold text-orange-600">{amount}</div>
    </div>
    '''

def render_submit_button(comp):
    """提交按钮"""
    label = comp.get("label", "提交")
    price = comp.get("price", "")
    return f'<button class="w-full bg-blue-500 text-white py-2 text-sm font-medium mb-2">{label} {price}</button>'

# ==============================================================================
# 意图澄清组件
# ==============================================================================

def render_tag_options(comp):
    """标签选项"""
    label = comp.get("label", "")
    options = comp.get("options", [])
    selected = comp.get("selected", None)
    html = f'<div class="border border-slate-200 p-3 mb-2">'
    html += f'<div class="text-xs font-medium text-slate-500 mb-2">{label}</div>' if label else ''
    html += '<div class="flex flex-wrap gap-2">'
    for opt in options:
        is_selected = (isinstance(selected, list) and opt in selected) or opt == selected
        if is_selected:
            html += f'<span class="bg-blue-500 text-white px-3 py-1 text-sm">{opt}</span>'
        else:
            html += f'<span class="bg-slate-100 text-slate-600 px-3 py-1 text-sm">{opt}</span>'
    html += '</div></div>'
    return html

def render_amount_option(comp):
    """金额选项"""
    label = comp.get("label", "选择金额")
    options = comp.get("options", [])
    selected = comp.get("selected", 0)
    html = f'<div class="border border-slate-200 p-3 mb-2"><div class="text-xs font-medium text-slate-500 mb-2">{label}</div><div class="flex gap-2">'
    for i, opt in enumerate(options):
        if i == selected:
            html += f'<span class="bg-blue-500 text-white px-3 py-1 text-sm">{opt}</span>'
        else:
            html += f'<span class="bg-slate-50 text-slate-600 px-3 py-1 text-sm">{opt}</span>'
    html += '</div></div>'
    return html

def render_list_option(comp):
    """列表选项"""
    label = comp.get("label", "")
    options = comp.get("options", [])
    selected = comp.get("selected", None)
    html = f'<div class="border border-slate-200 p-3 mb-2">'
    html += f'<div class="text-xs font-medium text-slate-500 mb-2">{label}</div>' if label else ''
    for i, opt in enumerate(options):
        title = opt.get("title", "")
        subtitle = opt.get("subtitle", "")
        is_selected = i == selected
        border = "border-blue-500 bg-blue-50" if is_selected else "border-slate-200"
        check = "●" if is_selected else "○"
        html += f'''
        <div class="border {border} p-2 mb-1 flex justify-between items-center">
            <div>
                <div class="text-sm text-slate-700">{title}</div>
                {f'<div class="text-xs text-slate-400">{subtitle}</div>' if subtitle else ''}
            </div>
            <span class="text-blue-500">{check}</span>
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
    <div class="border border-slate-200 p-3 mb-2 flex justify-between items-center">
        <span class="text-xs font-medium text-slate-500">{label}</span>
        <div class="flex items-center gap-2">
            <span class="w-6 h-6 bg-slate-100 text-center leading-6 text-sm">-</span>
            <span class="text-sm font-bold">{value}</span>
            <span class="w-6 h-6 bg-blue-500 text-white text-center leading-6 text-sm">+</span>
        </div>
        {f'<span class="text-xs text-slate-400">{unit}</span>' if unit else ''}
    </div>
    '''

def render_text_input(comp):
    """单行文本输入"""
    label = comp.get("label", "")
    placeholder = comp.get("placeholder", "请输入")
    value = comp.get("value", "")
    return f'''
    <div class="border border-slate-200 p-3 mb-2">
        {f'<div class="text-xs font-medium text-slate-500 mb-2">{label}</div>' if label else ''}
        <div class="bg-slate-50 p-2 text-sm text-slate-600">{value if value else placeholder}</div>
    </div>
    '''

def render_textarea_input(comp):
    """多行文本输入"""
    label = comp.get("label", "")
    placeholder = comp.get("placeholder", "请输入内容")
    value = comp.get("value", "")
    return f'''
    <div class="border border-slate-200 p-3 mb-2">
        {f'<div class="text-xs font-medium text-slate-500 mb-2">{label}</div>' if label else ''}
        <div class="bg-slate-50 p-2 text-sm text-slate-600 min-h-[60px]">{value if value else placeholder}</div>
    </div>
    '''

def render_phone_input(comp):
    """手机号码输入"""
    label = comp.get("label", "手机号码")
    placeholder = comp.get("placeholder", "请输入手机号")
    value = comp.get("value", "")
    return f'''
    <div class="border border-slate-200 p-3 mb-2">
        {f'<div class="text-xs font-medium text-slate-500 mb-2">{label}</div>' if label else ''}
        <div class="bg-slate-50 p-2 text-sm text-slate-600">{value if value else placeholder}</div>
    </div>
    '''

def render_amount_input(comp):
    """金额输入"""
    label = comp.get("label", "金额")
    placeholder = comp.get("placeholder", "0.00")
    value = comp.get("value", "")
    return f'''
    <div class="border border-slate-200 p-3 mb-2">
        {f'<div class="text-xs font-medium text-slate-500 mb-2">{label}</div>' if label else ''}
        <div class="bg-slate-50 p-2 text-sm text-slate-600">¥ {value if value else placeholder}</div>
    </div>
    '''

def render_confirm_button(comp):
    """确认按钮"""
    label = comp.get("label", "确认")
    disabled = comp.get("disabled", False)
    bg = "bg-slate-200 text-slate-400" if disabled else "bg-blue-500 text-white"
    return f'<button class="w-full {bg} py-2 text-sm font-medium mb-2">{label}</button>'

def render_text_link(comp):
    """文字链接"""
    text = comp.get("text", "查看详情")
    href = comp.get("href", "#")
    return f'<a href="{href}" class="text-sm text-blue-500 mb-2 block">{text}</a>'

def render_order_button(comp):
    """下单按钮"""
    label = comp.get("label", "立即下单")
    price = comp.get("price", "¥0")
    disabled = comp.get("disabled", False)
    bg = "bg-slate-200 text-slate-400" if disabled else "bg-blue-500 text-white"
    return f'<button class="w-full {bg} py-2 text-sm font-medium mb-2">{label} · {price}</button>'

def render_address_collector(comp):
    """收/寄件地址收集"""
    type_ = comp.get("type", "寄件")
    name = comp.get("name", "")
    phone = comp.get("phone", "")
    address = comp.get("address", "")
    return f'''
    <div class="border border-slate-200 p-3 mb-2">
        <div class="text-xs font-medium text-slate-500 mb-2">{type_}地址</div>
        <div class="space-y-2">
            <div class="bg-slate-50 p-2 text-sm text-slate-600">{name or "姓名"}</div>
            <div class="bg-slate-50 p-2 text-sm text-slate-600">{phone or "手机号"}</div>
            <div class="bg-slate-50 p-2 text-sm text-slate-600">{address or "详细地址"}</div>
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
    <div class="mb-2">
        <div class="flex items-center gap-2 mb-2 text-sm text-slate-600">
            <span class="text-blue-500">{check}</span>
            <span>同意{agreement}</span>
        </div>
        <button class="w-full bg-blue-500 text-white py-2 text-sm font-medium">{label}</button>
    </div>
    '''

def render_verify_button(comp):
    """核身按钮"""
    label = comp.get("label", "实名认证")
    agreement = comp.get("agreement", "《隐私协议》")
    checked = comp.get("checked", False)
    id_number = comp.get("idNumber", "")
    check = "☑" if checked else "☐"
    return f'''
    <div class="mb-2">
        <div class="flex items-center gap-2 mb-2 text-sm text-slate-600">
            <span class="text-blue-500">{check}</span>
            <span>同意{agreement}</span>
        </div>
        {f'<div class="bg-slate-50 p-2 text-sm text-slate-600 mb-2">{id_number or "身份证号"}</div>' if id_number is not None else ''}
        <button class="w-full bg-blue-500 text-white py-2 text-sm font-medium">{label}</button>
    </div>
    '''

def render_pay_button(comp):
    """支付按钮"""
    label = comp.get("label", "立即支付")
    amount = comp.get("amount", "¥0")
    disabled = comp.get("disabled", False)
    bg = "bg-slate-200 text-slate-400" if disabled else "bg-blue-500 text-white"
    return f'<button class="w-full {bg} py-2 text-sm font-medium mb-2">{label} · {amount}</button>'

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
        return f'<div class="border border-dashed border-slate-300 p-2 text-xs text-slate-400 mb-2">[{comp_type}]</div>'
    try:
        return renderer(comp)
    except Exception as e:
        return f'<div class="border border-red-200 bg-red-50 p-2 text-xs text-red-400 mb-2">error: {comp_type}</div>'

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
</head>
<body class="bg-white p-3 text-sm">
    {content}
</body>
</html>'''