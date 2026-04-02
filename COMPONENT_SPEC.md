# A2UI 组件设计规范

> 基于 Apple iOS Human Interface Guidelines，目标设备 iPhone 17 Pro (393 x 852 pt)
> 本文档是组件视觉样式的唯一参照标准，所有修改需同步更新此文档与 `components.py`

---

## 1 全局设计令牌

### 1.1 色板

| 令牌 | 值 | Tailwind class | 用途 |
|---|---|---|---|
| ios-blue | `#007AFF` | `text-ios-blue` / `bg-ios-blue` | 主操作、选中态、链接 |
| ios-green | `#34C759` | `text-ios-green` | 完成/成功状态 |
| ios-orange | `#FF9500` | `text-ios-orange` | 价格、优惠、警告 |
| ios-red | `#FF3B30` | `text-ios-red` | 错误 |
| ios-label | `#000000` | `text-ios-label` | 主标签，标题/正文 |
| ios-label-2 | `#8E8E93` | `text-ios-label-2` | 次要文字，副标题/说明 |
| ios-label-3 | `#C7C7CC` | `text-ios-label-3` | 占位符/禁用文字 |
| ios-separator | `#C6C6C8` | `border-ios-separator` | 分割线、次按钮边框 |
| ios-bg-2 | `#F2F2F7` | `bg-ios-bg-2` | 输入框底色、分组背景 |
| ios-fill | `#E5E5EA` | `bg-ios-fill` | 未选中标签、禁用按钮 |

### 1.2 字号阶梯

| 名称 | size | line-height | weight | Tailwind | 适用场景 |
|---|---|---|---|---|---|
| **headline** | 17px | 22px | semibold (600) | `text-[17px] leading-[22px] font-semibold` | 标题、按钮文字 |
| **body** | 17px | 22px | regular (400) | `text-[17px] leading-[22px]` | 正文内容、数值 |
| **subhead** | 15px | 20px | regular (400) | `text-[15px] leading-[20px]` | 卡片正文、协议文字 |
| **footnote** | 13px | 18px | regular/medium | `text-[13px] leading-[18px]` | 辅助说明、表头、标签名 |
| **caption1** | 12px | 16px | regular/medium | `text-[12px] leading-[16px]` | 极小标签、类型标记 |

### 1.3 间距网格

| 用途 | 值 | Tailwind |
|---|---|---|
| 组件外间距 (底部) | 12px | `mb-3` |
| 容器内间距 | 16px | `p-4` |
| 子元素间距 (紧凑) | 8px | `gap-2` / `mb-2` / `mt-1` / `space-y-2` |
| 子元素间距 (宽松) | 12px | `gap-3` / `mb-3` |
| 输入框内间距 | 12px | `p-3` |

### 1.4 圆角

| 名称 | 值 | Tailwind | 用途 |
|---|---|---|---|
| ios | 10px | `rounded-ios` | 卡片、按钮、时间选项卡 |
| ios-sm | 8px | `rounded-ios-sm` | 输入框 |
| full | 9999px | `rounded-full` | 药丸标签、步进器按钮、头像 |

### 1.5 阴影

| 名称 | 值 | Tailwind |
|---|---|---|
| ios | `0 1px 3px rgba(0,0,0,0.08)` | `shadow-ios` |

### 1.6 可复用容器模式

后续组件规格中以 **粗体名称** 引用以下模式：

| 模式 | 样式 | 说明 |
|---|---|---|
| **Card** | `bg-white rounded-ios shadow-ios p-4 mb-3` | 标准卡片容器 |
| **InputField** | `bg-ios-bg-2 rounded-ios-sm p-3 subhead` | 输入框内部 |
| **PillSelected** | `bg-ios-blue text-white px-4 py-2 rounded-full subhead` | 选中药丸标签 |
| **PillDefault** | `bg-ios-fill text-ios-label px-4 py-2 rounded-full subhead` | 未选中药丸标签 |
| **PrimaryBtn** | `w-full bg-ios-blue text-white py-3 headline rounded-ios min-h-[44px] mb-3` | 主按钮 |
| **DisabledBtn** | `w-full bg-ios-fill text-ios-label-3 py-3 headline rounded-ios min-h-[44px] mb-3` | 禁用按钮 |
| **SecondaryBtn** | `flex-1 border border-ios-separator text-ios-label py-3 headline rounded-ios min-h-[44px]` | 次按钮 |

### 1.7 字体栈

```
-apple-system, "SF Pro Text", "SF Pro Display", system-ui, sans-serif
```

---

## 2 展示类组件

### Heading
> 标题 · 展示类 · 通用

页面标题组件，用于在内容顶部显示一级标题。适合作为一个回复卡片的开头，概括当前内容主题。AI 回复中当需要为一段内容加上总结性标题时使用，例如「快递寄送服务」「账单详情」。

**渲染** `<h2>` headline · ios-label · mb-3

Props: `text`(string)

---

### Paragraph
> 段落文本 · 展示类 · 通用

正文段落组件，用于展示一段说明性文字。适合对服务、规则、注意事项进行简要文字描述，常跟在 Heading 之后作为正文内容。当 AI 需要向用户解释一段信息但不需要结构化 UI 时使用。

**渲染** `<p>` subhead · ios-label-2 · mb-3

Props: `text`(string)

---

### InfoTable
> 信息表格 · 展示类 · 通用

信息表格组件，以表格形式展示结构化数据。适合对比多项信息，如基金列表、费率对比、套餐方案等。当信息有多个维度且需要横向对比时，优先选择此组件。表头固定在顶部，数据行按行交替展示。

**容器** `bg-white rounded-ios shadow-ios mb-3 overflow-hidden`
**表头** footnote · ios-label-2 · font-normal · px-4 py-3 · 底部 border-ios-separator
**单元格** subhead · ios-label · px-4 py-3 · 底部 border-ios-separator/30

Props: `headers`(string[]), `rows`({name, rate, feature}[])

---

### PriceCard
> 价格卡片 · 展示类 · 通用

价格卡片组件，带「费用明细」标题的价格分项列表，底部显示合计金额（橙色高亮）。适合展示订单费用构成，如运费、包装费、保价费等。用户在确认下单前需要了解价格组成时使用，通常放在按钮组件之前。

**容器** Card
**标题** footnote · font-semibold · ios-label-2 · mb-3 · 固定文字"费用明细"
**行项** subhead · flex justify-between · mb-2 · label=ios-label-2 value=ios-label
**合计行** subhead · font-semibold · border-t border-ios-separator · pt-3 mt-3 · value=font-bold ios-orange

Props: `items`({label,value}[]), `total`(string)

---

## 3 输入/选择类组件

### AddressInput
> 地址输入 · 输入选择类 · 行业特定

地址输入组件，提供一个地址文本输入区域。用户可手动填写或从地址簿选择。适合需要用户提供地址的场景，如寄件地址、收货地址等。输入框为浅灰底色的圆角矩形，未填写时显示占位提示文字。

**容器** Card
**label** footnote · font-medium · ios-label-2 · mb-2
**输入框** InputField · 有值=ios-label · 无值=ios-label-3

Props: `label`(string?), `placeholder`(string?), `value`(string?)

---

### ContactInput
> 联系人输入 · 输入选择类 · 行业特定

联系人输入组件，包含姓名和电话两个字段，用竖线分隔显示在同一行。适合在寄件、预约等场景收集联系人信息。当姓名和电话需要成对出现时使用此组件，而非分开使用两个 TextInput。

**容器** Card
**label** footnote · font-medium · ios-label-2 · mb-2
**内容** subhead · name 和 phone 用 `|`(ios-separator色) 分隔 · 有值=ios-label · 无值=ios-label-3

Props: `label`(string="联系人"), `name`(string?), `phone`(string?)

---

### TagOptions
> 标签选项 · 输入选择类 · 通用

标签选项组件，以可换行的药丸标签按钮组让用户选择一个或多个选项。这是最通用的意图澄清组件，适合场景分类、偏好选择、功能入口等。选中项为蓝底白字，未选中项为灰底黑字。当 AI 需要用户从几个选项中明确意图时首选此组件。

**容器** Card
**label** footnote · font-medium · ios-label-2 · mb-3
**选项** flex flex-wrap gap-2 · 选中=PillSelected · 未选中=PillDefault

Props: `label`(string?), `options`(string[]), `selected`(string|string[]|null)

---

### AmountOption
> 金额选项 · 输入选择类 · 通用

金额选项组件，以横向药丸标签展示预设金额选项。适合话费充值、红包金额、转账金额等需要从固定金额中快速选择的场景。视觉上与 TagOptions 一致，但语义上专用于金额选择。

**容器** Card
**label** footnote · font-medium · ios-label-2 · mb-3
**选项** flex flex-wrap gap-2 · 选中=PillSelected · 未选中=PillDefault

Props: `label`(string="选择金额"), `options`(string[]), `selected`(number=0)

---

### ListOption
> 列表选项 · 输入选择类 · 通用

列表选项组件，每个选项为带标题和副标题的卡片式条目，右侧有单选圆点指示符。适合在多个方案/服务中选择一项，如快递公司选择、保险方案对比等。当选项需要更丰富的描述信息（标题+副标题）时使用此组件，而非 TagOptions。

**容器** Card
**label** footnote · font-medium · ios-label-2 · mb-3
**每项** `border rounded-ios p-3 mb-2 flex justify-between items-center min-h-[44px]`
**选中** border-ios-blue bg-blue-50 · 指示符 `●` ios-blue
**未选中** border-ios-separator/50 · 指示符 `○` ios-blue
**title** subhead · ios-label
**subtitle** footnote · ios-label-2

Props: `label`(string?), `options`({title,subtitle}[]), `selected`(number|null)

---

### Stepper
> 步进器 · 输入选择类 · 通用

步进器组件，带 +/- 圆形按钮的数值调节器。左侧显示标签，右侧是减号按钮、当前数值、加号按钮。适合调整数量、重量、份数等数值型输入，用户可通过按钮快速增减而无需手动输入。

**容器** Card · flex justify-between items-center · min-h-[44px]
**label** subhead · ios-label-2
**减按钮** `w-8 h-8 bg-ios-fill rounded-full` · body · ios-label · 字符 `−`
**值** body · font-semibold · ios-label
**加按钮** `w-8 h-8 bg-ios-blue rounded-full` · body · text-white · 字符 `+`
**unit** footnote · ios-label-2

Props: `label`(string), `value`(number=1), `unit`(string?)

---

### TextInput
> 单行输入 · 输入选择类 · 通用

单行文本输入组件，提供一个简单的文本输入框。适合收集短文本信息，如姓名、快递单号、验证码等。当需要用户输入一行自由文本时使用，输入框为浅灰底色圆角矩形。

**容器** Card
**label** footnote · font-medium · ios-label-2 · mb-2
**输入框** InputField · 有值=ios-label · 无值=ios-label-3

Props: `label`(string?), `placeholder`(string="请输入"), `value`(string?)

---

### TextareaInput
> 多行输入 · 输入选择类 · 通用

多行文本输入组件，提供一个可输入多行文字的区域（最小高度 80px）。适合收集备注、留言、问题描述等较长文本。当预期用户输入内容超过一行时使用此组件替代 TextInput。

**容器** Card
**label** footnote · font-medium · ios-label-2 · mb-2
**输入框** InputField · min-h-[80px] · 有值=ios-label · 无值=ios-label-3

Props: `label`(string?), `placeholder`(string="请输入内容"), `value`(string?)

---

### PhoneInput
> 手机号输入 · 输入选择类 · 通用

手机号码输入组件，专用于手机号收集。视觉上与 TextInput 一致，但语义上明确标识为手机号输入，便于前端做格式校验和键盘适配。适合注册、验证身份、联系人信息填写等场景。

**容器** Card
**label** footnote · font-medium · ios-label-2 · mb-2
**输入框** InputField · 有值=ios-label · 无值=ios-label-3

Props: `label`(string="手机号码"), `placeholder`(string="请输入手机号"), `value`(string?)

---

### AmountInput
> 金额输入 · 输入选择类 · 通用

金额输入组件，带 ¥ 前缀的金额输入框。适合自定义转账金额、充值金额、还款金额等需要用户手动输入精确金额的场景。当预设金额选项不能满足需求时，用此组件配合 AmountOption 使用。

**容器** Card
**label** footnote · font-medium · ios-label-2 · mb-2
**输入框** InputField · 前缀 `¥` · 有值=ios-label · 无值=ios-label-3

Props: `label`(string="金额"), `placeholder`(string="0.00"), `value`(string?)

---

## 4 按钮类组件

### ActionButton
> 操作按钮组 · 按钮类 · 通用

操作按钮组组件，可在一行内横向放置多个按钮。支持 primary（蓝底白字主按钮）和 secondary（白底灰框次按钮）两种样式。适合同时提供「确认」和「取消」、「同意」和「拒绝」等多个并列操作选项。

**容器** `flex gap-3 mb-3`
**primary** PrimaryBtn（改 `flex-1` 替代 `w-full`）
**secondary** SecondaryBtn

Props: `actions`({label, type:"primary"|"secondary"}[])

---

### ConfirmButton
> 确认按钮 · 按钮类 · 通用

确认按钮组件，全宽蓝色主按钮。这是最基础的操作按钮，适合表单提交、流程确认等单一操作场景。可通过 disabled 属性控制按钮是否可点击（禁用时变为灰色）。当只需要一个操作按钮时首选此组件。

**启用** PrimaryBtn
**禁用** DisabledBtn

Props: `label`(string="确认"), `disabled`(bool=false)

---

### SubmitButton
> 提交按钮 · 按钮类 · 通用

提交按钮组件，全宽蓝色按钮，可在按钮文字后附带金额显示。适合提交表单、提交申请等场景。与 ConfirmButton 的区别在于可以附带价格信息。

**渲染** PrimaryBtn · 文字 `{label} {price}`

Props: `label`(string="提交"), `price`(string?)

---

### OrderButton
> 下单按钮 · 按钮类 · 通用

下单按钮组件，全宽蓝色按钮，按钮文字中用 · 分隔展示操作文字和价格。适合购物、寄件等需要在按钮上同时展示操作和总价的下单确认场景，让用户一目了然地看到操作和费用。支持 disabled 属性。

**启用** PrimaryBtn · 文字 `{label} · {price}`
**禁用** DisabledBtn

Props: `label`(string="立即下单"), `price`(string="¥0"), `disabled`(bool=false)

---

### PayButton
> 支付按钮 · 按钮类 · 通用

支付按钮组件，全宽蓝色按钮，显示支付金额。适合支付确认页的最终操作按钮，如话费充值确认、订单支付等。语义上明确表示这是一个会触发支付行为的按钮。

**启用** PrimaryBtn · 文字 `{label} · {amount}`
**禁用** DisabledBtn

Props: `label`(string="立即支付"), `amount`(string="¥0"), `disabled`(bool=false)

---

### TextLink
> 文字链接 · 按钮类 · 通用

文字链接组件，以蓝色文字链接形式展示。适合「查看详情」「了解更多」「查看完整协议」等辅助跳转操作，不占据主视觉焦点。通常放在页面底部或正文之后作为补充入口。

**渲染** `<a>` subhead · ios-blue · mb-3 block

Props: `text`(string="查看详情"), `href`(string="#")

---

### AuthButton
> 授权按钮 · 按钮类 · 通用

授权按钮组件，包含协议勾选框和授权按钮两部分。用户需先勾选同意协议后才能点击操作按钮。适合开通服务、签约代扣、授权访问等需要用户明确同意协议条款的场景。勾选框使用蓝色打勾图标。

**容器** mb-3
**协议行** flex items-center gap-2 · mb-3 · subhead · ios-label-2
**勾选框** `☑`/`☐` ios-blue
**按钮** PrimaryBtn（无 mb-3）

Props: `label`(string="同意并授权"), `agreement`(string="《用户协议》"), `checked`(bool=false)

---

### VerifyButton
> 核身按钮 · 按钮类 · 通用

核身验证按钮组件，包含协议勾选、身份证号输入框和验证按钮三部分。这是安全级别最高的操作组件，适合实名认证、身份核验等需要提交身份信息的场景。身份证输入框位于协议行和按钮之间。

**容器** mb-3
**协议行** 同 AuthButton
**身份证输入** InputField · mb-3 · 有值=ios-label · 无值=ios-label-3
**按钮** PrimaryBtn（无 mb-3）

Props: `label`(string="实名认证"), `agreement`(string="《隐私协议》"), `checked`(bool=false), `idNumber`(string?)

---

## 5 聊天界面 (render_chat_html)

全部使用内联样式，不依赖 Tailwind class。

### 5.1 整体容器

`padding: 16px 12px 20px 12px`

### 5.2 用户消息（右对齐）

| 元素 | 样式 |
|---|---|
| 气泡背景 | `#007AFF` |
| 气泡文字 | `#fff`, 17px, line-height 1.4 |
| 气泡圆角 | 18px |
| 气泡内边距 | 10px 16px |
| 气泡最大宽度 | 75% |
| 三角箭头 | 右侧 6px, `#007AFF` |
| 头像 | 36x36, `border-radius:50%`, 渐变 `#5AC8FA → #007AFF`, 文字 "Me" 14px 600 |

### 5.3 Agent 回复（左对齐）

| 元素 | 样式 |
|---|---|
| 头像 | 36x36, `border-radius:50%`, 渐变 `#5856D6 → #AF52DE`, 文字 "AI" 14px |
| 气泡背景 | `#fff` |
| 气泡圆角 | 18px |
| 气泡内边距 | 12px 16px |
| 气泡最大宽度 | 80% |
| 三角箭头 | 左侧 6px, `#fff` |
| 文字区 | 17px, line-height 1.4, `#000` |
| 组件区 | margin-top 8px（文字区存在时），否则 0 |

### 5.4 simple_markdown 内联样式

| 元素 | 样式 |
|---|---|
| `<p>` | `margin:8px 0; color:#000; font-size:17px; line-height:1.4` |
| `<ul>` | `margin:8px 0; padding-left:20px` |
| `<li>` | `margin:4px 0; color:#000; font-size:17px; line-height:1.4` |

---

## 6 手机模拟器 (app_v2.py)

| 参数 | 值 |
|---|---|
| 设备 | iPhone 17 Pro |
| 屏幕尺寸 | 393 x 852 pt |
| 外壳边距 | 10px |
| 外壳总尺寸 | 413 x 872 px |
| 屏幕圆角 | 52px |
| 外壳圆角 | 60px |
| 缩放比例 | 0.775 (transform: scale) |
| 灵动岛 | 126 x 37, 圆角 20px |
| 导航栏 | 17px 600, 背景 #F2F2F7 |
| 聊天背景 | #F2F2F7 |
| 输入栏 | 17px, 圆角 20px, 占位色 #C7C7CC |
| 发送按钮 | 34x34, #007AFF, 圆形, SVG 箭头 |
| Home 指示条 | 134 x 5, 圆角 3px, opacity 0.25 |
