import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import html
import os

# ==============================================================================
# 1. 配置与高保真模板
# ==============================================================================
st.set_page_config(layout="wide", page_title="高保真效果对比")

# 数据路径 (请修改为您实际的文件路径)
INPUT_CSV_PATH = "/Users/shangguan/PycharmProjects/workbench/data_files/10goodcase.csv"
OUTPUT_CSV_PATH = INPUT_CSV_PATH.replace(".csv", "_labeled_versions.csv")

# === 您的新 HTML 模板 ===
HTML_TEMPLATE_STR = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jinni 模版 - 横向滑动表格版</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700&display=swap" rel="stylesheet">
    <style>
        /* =========================================
           1. 基础环境设置 (仿真器布局核心)
           ========================================= */
        html { 
            font-size: 100px !important; /* 定义 REM 基准 */
            box-sizing: border-box;
        }
        *, ::after, ::before { box-sizing: inherit; }

        body {
            margin: 0; 
            background-color: #e5e5e5; 
            min-height: 100vh;
            display: flex; 
            justify-content: center; 
            align-items: center;
            font-family: 'PingFang SC', -apple-system, BlinkMacSystemFont, sans-serif;
            padding: 20px 0; 
            overflow-y: auto;
        }

        .preview-wrapper {
            width: 375px; 
            height: 812px; 
            position: relative;
            box-shadow: 0 40px 100px rgba(0,0,0,0.2); 
            border-radius: 40px; 
            background: #fff;
            overflow: hidden; 
        }

        .phone-simulator {
            width: 750px; 
            height: 1624px; 
            background-color: #F5F7FA;
            position: absolute; 
            top: 0; 
            left: 0; 
            overflow: hidden;
            display: flex; 
            flex-direction: column;
            transform: scale(0.5); 
            transform-origin: 0 0;
        }

        .status-bar { 
            height: 88px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 32px; 
            font-weight: bold; 
            background: rgba(255,255,255,0.95); 
            z-index: 10; 
            flex-shrink: 0; 
            border-bottom: 1px solid rgba(0,0,0,0.03); 
        }

        .scroll-area { 
            flex: 1; 
            overflow-y: auto; 
            padding: 32px; 
        }
        .scroll-area::-webkit-scrollbar { display: none; }

        /* =========================================
           2. 聊天气泡 (上下文)
           ========================================= */
        .chat-row { display: flex; margin-bottom: 40px; align-items: flex-start; }
        .chat-row.right { justify-content: flex-end; }
        .chat-row.left { justify-content: flex-start; }

        .chat-bubble { 
            max-width: 70%; 
            padding: 24px 32px; 
            border-radius: 32px; 
            font-size: 30px; 
            line-height: 1.5; 
            position: relative; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
            word-wrap: break-word;
        }
        .chat-row.right .chat-bubble { background: #1677ff; color: #fff; margin-right: 20px; border-top-right-radius: 8px; }
        .chat-row.left .chat-bubble { background: #fff; color: #333; margin-left: 20px; border-top-left-radius: 8px; }

        .avatar { 
            width: 80px; height: 80px; 
            border-radius: 50%; 
            background: #ddd; 
            flex-shrink: 0; 
            border: 2px solid #fff; 
            overflow: hidden; 
        }
        .avatar img { width: 100%; height: 100%; object-fit: cover; }

        /* =========================================
           3. AI 回答内容容器 (Core Response Styles)
           ========================================= */
        .response-container {
            width: 100%; 
            background: #fff; 
            border-radius: 36px; 
            padding: 40px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.04); 
            box-sizing: border-box;
            font-size: 28px; 
            color: #333; 
            margin-bottom: 40px;
        }

        /* --- 标题 --- */
        .response-container h1 {
            font-family: 'Noto Serif SC', serif; 
            font-size: 48px; 
            line-height: 1.4;
            margin: 0 0 32px 0; 
            color: #333; 
            font-weight: normal;
        }
        .response-container h2 {
            display: flex;
            align-items: center;
            font-size: 32px;
            font-weight: 700;
            margin: 40px 0 24px 0;
        }
        /* 序号标签 */
        .response-container h2 .label {
            display: inline-block;
            margin-right: 16px;
            width: 40px; height: 40px;
            color: #1677ff;
            border-radius: 10px;
            font-size: 24px;
            text-align: center;
            line-height: 40px;
            background: rgba(22, 119, 255, 0.1);
            flex-shrink: 0;
        }

        /* --- 段落与链接 --- */
        .response-container p {
            font-size: 30px; 
            line-height: 1.6; 
            margin: 0 0 24px 0; 
            text-align: justify; 
            color: #333;
        }
        .response-container .inline-link {
            color: #1677ff; 
            font-weight: 500; 
            text-decoration: none; 
            cursor: pointer;
            display: inline-flex; 
            align-items: center; 
            margin: 0 4px; 
            vertical-align: baseline;
        }
        /* --- 引用块 --- */
        .response-container blockquote {
            margin: 32px 0; padding-left: 24px;
            border-left: 6px solid #E5E5E5; color: #666;
            font-size: 30px; line-height: 1.6;
        }

        /* =========================================
           4. 表格组件核心样式 (智能自适应版)
           ========================================= */
        /* --- 4.1 外层卡片容器 (滑动窗口) --- */
        .table-card {
            border: 2px solid #eee;
            border-radius: 32px;
            margin-bottom: 48px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.02);
            background: #fff;

            /* 开启横向滚动 */
            overflow-x: auto;
            -webkit-overflow-scrolling: touch; 
            scrollbar-width: none; 
        }
        .table-card::-webkit-scrollbar { display: none; }

        /* --- 4.2 表格全局 --- */
        table {
            table-layout: auto;    /* 自动分配列宽 */
            width: 100%;           /* 默认占满容器 */
            border-collapse: collapse;
            font-size: 30px;
        }

        /* --- 4.3 单元格通用设置 --- */
        th, td {
            min-width: 260px;     /* 普通列至少260px宽 */
            padding: 32px 30px;   
            border-bottom: 2px solid #f0f0f0;
            vertical-align: top;
            line-height: 1.6;
            color: #333;
        }

        /* --- 4.4 表头特有 --- */
        thead th {
            background-color: #f7f8fa;
            color: #999;
            font-weight: 400;
            font-size: 24px;
            padding: 24px 30px;
            text-align: left;
            border-bottom: 2px solid #eee;
            white-space: nowrap; 
        }

        /* --- 4.5 第一列特有样式 (人名列) --- */
        th:first-child,
        td:first-child {
            background-color: #fafafa;
            border-right: 2px solid #f0f0f0;
            min-width: 140px; 
            width: auto;
            text-align: center;
            white-space: nowrap; 
        }

        /* 第一列的内容样式 */
        td:first-child {
            font-weight: 700;
            font-size: 32px;
            color: #555;
        }

        /* --- 4.6 细节修饰 --- */
        td:last-child { border-right: none; }
        tr:last-child td { border-bottom: none; }

        .sub-text {
            display: block;
            font-size: 24px;
            color: #999;
            font-weight: 400;
            margin-top: 8px;
        }

        /* --- 列表与卡片等其他样式 --- */
        .response-container ul { margin: 24px 0 48px 0; padding-left: 40px; list-style-type: disc; }
        .response-container li { margin-bottom: 24px; font-size: 30px; line-height: 1.6; color: #333; text-align: justify; }

        /* --- 图表卡片 --- */
        .chart-card {
            border: 1px solid #F0F0F0; border-radius: 24px; padding: 32px;
            margin-top: 32px; background: #fff;
        }
        .chart-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 20px; }
        .chart-title { font-size: 32px; font-weight: bold; color: #333; }
        .chart-subtitle { font-size: 24px; color: #999; }
        .chart-canvas-wrapper { position: relative; height: 320px; width: 100%; }
        .chart-footer { margin-top: 24px; font-size: 22px; color: #ccc; text-align: right; }
    </style>
</head>
<body>
    <div class="preview-wrapper">
        <div class="phone-simulator">
            <div class="status-bar">9:41</div>
            <div class="scroll-area">

                <div class="chat-row right">
                    <div class="chat-bubble">__QUERY__</div>
                    <div class="avatar"><img src="https://api.iconify.design/fluent-emoji:person-raising-hand.svg" alt=""></div>
                </div>

                __INTRO_BLOCK__

                <div class="response-container">
                    __MAIN_CONTENT__
                </div>

                __OUTRO_BLOCK__

                <div style="height: 60px;"></div>
            </div>
        </div>
    </div>
</body>
</html>
"""


# ==============================================================================
# 2. 核心逻辑函数
# ==============================================================================

def generate_full_html(query, intro, main_content, outro):
    """根据各部分片段拼装完整 HTML"""
    # 处理空值
    intro = "" if pd.isna(intro) else str(intro)
    main_content = "" if pd.isna(main_content) else str(main_content)
    outro = "" if pd.isna(outro) else str(outro)
    query = "" if pd.isna(query) else str(query)

    # 1. 构造 Intro HTML
    intro_block = ""
    if intro.strip():
        intro_block = f"""
        <div class="chat-row left">
            <div class="avatar"><img src="https://api.iconify.design/fluent-emoji:woman-technologist.svg" alt=""></div>
            <div class="chat-bubble">{html.escape(intro)}</div>
        </div>
        """

    # 2. 构造 Outro HTML
    outro_block = ""
    if outro.strip():
        outro_block = f"""
        <div class="chat-row left" style="margin-top: 20px;">
            <div class="avatar"><img src="https://api.iconify.design/fluent-emoji:woman-technologist.svg" alt=""></div>
            <div class="chat-bubble">{html.escape(outro)}</div>
        </div>
        """

    # 3. 处理核心内容 (中间8)
    # 关键修改：将表格外层包裹 class 修改为 "table-card"，以匹配新 CSS 实现横滑
    # 注意：如果您的原始数据已经是完整的 <table>...</table>，则直接包裹
    # 如果原始数据里已经有 div class="table-card"，则不需要重复
    processed_main = main_content

    # 简单检测并替换，确保表格被 table-card 包裹
    if '<table' in processed_main and 'table-card' not in processed_main:
        processed_main = processed_main.replace('<table', '<div class="table-card"><table')
        processed_main = processed_main.replace('</table>', '</table></div>')

    # 替换模板占位符
    final_html = HTML_TEMPLATE_STR.replace('__QUERY__', html.escape(query))
    final_html = final_html.replace('__INTRO_BLOCK__', intro_block)
    final_html = final_html.replace('__MAIN_CONTENT__', processed_main)
    final_html = final_html.replace('__OUTRO_BLOCK__', outro_block)

    return final_html


@st.cache_data
def load_data():
    if not os.path.exists(INPUT_CSV_PATH):
        return None
    return pd.read_csv(INPUT_CSV_PATH)


def save_labels(df):
    """保存标记结果"""
    # 将 session 中的标记更新到 dataframe
    for idx, best_ver in st.session_state['best_versions'].items():
        if idx in df.index:
            df.at[idx, 'best_version_selected'] = best_ver

    df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8-sig')
    st.toast(f"✅ 保存成功! {OUTPUT_CSV_PATH}")


# ==============================================================================
# 3. Streamlit UI
# ==============================================================================

if 'best_versions' not in st.session_state:
    st.session_state['best_versions'] = {}


def main():
    st.title("📱 仿真器多版本对比 (横滑表格版)")

    df_origin = load_data()
    if df_origin is None:
        st.error(f"找不到文件: {INPUT_CSV_PATH}")
        return

    df = df_origin.copy()

    # 1. 自动识别版本列
    version_cols = [c for c in df.columns if c.startswith("8部分内容_")]

    # 侧边栏控制
    with st.sidebar:
        st.header("控制面板")

        # Query 导航
        query_options = df.index.tolist()
        selected_index = st.selectbox(
            "选择第几条数据 (Index)",
            options=query_options,
            format_func=lambda x: f"[{x}] {str(df.loc[x, 'query'])[:15]}..."
        )

        st.divider()
        st.subheader("选择要对比的版本")
        # 默认选中前两个版本进行对比
        default_versions = version_cols[:2] if len(version_cols) >= 2 else version_cols
        selected_versions = st.multiselect(
            "勾选需要展示的版本列",
            options=version_cols,
            default=default_versions
        )

        st.divider()
        if st.button("💾 保存打标结果", type="primary"):
            save_labels(df)

    # 主区域
    if selected_index is not None:
        row = df.loc[selected_index]

        # 显示当前上下文信息
        with st.expander("📝 查看 Query 基础信息", expanded=False):
            col1, col2 = st.columns([1, 3])
            col1.info(f"**Index**: {selected_index}")
            col1.markdown(f"**类型**: {row.get('类型', 'N/A')}")
            col2.markdown(f"**Query**: {row.get('query', '')}")
            st.text(f"修改意见: {row.get('修改意见', '无')}")

        st.divider()

        if not selected_versions:
            st.warning("请在左侧侧边栏至少选择一个版本进行查看。")
            return

        # 动态创建列
        cols = st.columns(len(selected_versions))

        # 遍历选中的版本列进行渲染
        for i, ver_col in enumerate(selected_versions):
            with cols[i]:
                # 标题
                st.subheader(f"📺 {ver_col}")

                # 提取各部分数据
                q_text = row.get('query', '')
                intro_text = row.get('前1', '')
                outro_text = row.get('后1', '')
                mid_content = row.get(ver_col, '')

                # 拼装
                html_code = generate_full_html(q_text, intro_text, mid_content, outro_text)

                # 渲染: 高度设为 850 以完整展示仿真器
                if pd.isna(mid_content) or str(mid_content).strip() == "":
                    st.warning("内容为空")
                else:
                    components.html(html_code, height=860, width=420, scrolling=False)

                # 打标按钮
                is_best = st.session_state['best_versions'].get(selected_index) == ver_col
                btn_type = "primary" if is_best else "secondary"
                btn_label = "✅ 已选为最佳" if is_best else f"🏆 选为最佳 ({ver_col})"

                if st.button(btn_label, key=f"btn_{selected_index}_{ver_col}", type=btn_type):
                    st.session_state['best_versions'][selected_index] = ver_col
                    st.rerun()


if __name__ == "__main__":
    main()