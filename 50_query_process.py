import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import time
import model  # 确保 model.py 在同级目录下
from datetime import datetime
import os

# 1. 页面配置
st.set_page_config(layout="wide", page_title="Test Cases Preview")

# ==============================================================================
# CSS 样式区域
# ==============================================================================
st.markdown("""
<style>
    /* 1. 整体页面背景：浅灰色 */
    .stApp { background-color: #F2F3F5; }

    /* 2. 卡片样式：针对 st.container(border=True) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #E5E5E5 !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* 3. 字体颜色修正 */
    .stMarkdown, .stText, h1, h2, h3, p, li, span { color: #333333 !important; }

    /* 4. 蓝色气泡文字颜色保护 */
    .user-bubble-content { color: #FFFFFF !important; }

    /* 5. 隐藏头部 */
    header[data-testid="stHeader"] { background-color: transparent; }
</style>
""", unsafe_allow_html=True)

# 2. 加载数据 (增加容错)
file_path = "/Users/shangguan/PycharmProjects/workbench/data_files/300query_processed.csv"

try:
    if not os.path.exists(file_path):
        st.error(f"文件不存在: {file_path}")
        st.stop()

    test_case = pd.read_csv(file_path)
    # 确保 query 列不为空
    test_case = test_case.dropna(subset=['query'])

except Exception as e:
    st.error(f"读取数据失败: {e}")
    st.stop()

# ==============================================================================
# 【核心逻辑修改】智能确定目标列名
# ==============================================================================

# 1. 找出所有以 "8部分内容_" 开头的现有列
existing_content_cols = [c for c in test_case.columns if str(c).startswith("8部分内容_")]

target_column_name = ""
need_new_column = True  # 默认假设需要新建

if existing_content_cols:
    # 取最后一列（假设按创建顺序排列，通常read_csv会保留列顺序）
    last_col = existing_content_cols[-1]

    # 2. 检查这一列是否已填满
    # 逻辑：只要存在 NaN 或者 空字符串，就视为未完成
    # .all() 为 True 表示所有行都有值，则已完成
    is_complete = test_case[last_col].apply(lambda x: pd.notna(x) and str(x).strip() != "").all()

    if not is_complete:
        # 如果未完成，则锁定这一列继续跑
        target_column_name = last_col
        need_new_column = False
        st.toast(f"检测到上次未完成的任务，继续填充列: {target_column_name}", icon="🔄")
    else:
        # 如果已完成，准备新建
        st.toast(f"上一轮任务 {last_col} 已全部完成，准备开启新任务", icon="✅")

# 3. 如果需要新建列
if need_new_column:
    # 只有确实要新建时才生成时间戳
    if 'run_timestamp' not in st.session_state:
        st.session_state['run_timestamp'] = datetime.now().strftime("%m%d_%H%M")

    target_column_name = f"8部分内容_{st.session_state['run_timestamp']}"

    # 初始化该列（如果在df中不存在）
    if target_column_name not in test_case.columns:
        test_case[target_column_name] = ""
        # 立即保存一次结构，防止刷新后找不到列
        test_case.to_csv(file_path, index=False, encoding='utf-8-sig')

# 3. 加载 Prompt
prompt_path = '/Users/shangguan/PycharmProjects/workbench/prompt/sp_for_50_query_1230.md'
try:
    with open(prompt_path, 'r', encoding='utf-8') as f:
        system_prompt_1225 = f.read()
except FileNotFoundError:
    st.error(f"Prompt文件找不到: {prompt_path}")
    st.stop()

# 页面标题
st.header("Test Cases for System Prompt 1230")
# 显示当前正在工作的列
st.caption(f"Generated with `Qwen3-235B` | **Current Target Column:** `{target_column_name}`")

cols = st.columns(4)

# 4. 循环渲染
for i, (index, row) in enumerate(test_case.iterrows()):
    current_col = cols[i % 4]

    with current_col:
        with st.container(border=True):

            # --- A. 用户 Query (蓝色气泡) ---
            st.markdown(
                f"""
                <div style="width: 100%; display: flex; justify-content: flex-end; margin-bottom: 10px;">
                    <div style="
                        background-color: #007AFF; 
                        padding: 10px 15px; 
                        border-radius: 15px 15px 0 15px; 
                        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                        max-width: 90%;
                    ">
                        <span class="user-bubble-content" style="color: #FFFFFF; font-size: 14px;">{row['query']}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # --- B. 助手回复 ---
            with st.chat_message("assistant", avatar="🤖"):

                # 1. 前言
                if pd.notna(row.get('前言1')):
                    st.markdown(row['前言1'])

                # 2. HTML 卡片生成与保存
                html_content = ""

                # 【缓存检查逻辑】
                # 检查当前行的目标列是否有内容
                raw_content = row.get(target_column_name)
                already_generated = pd.notna(raw_content) and str(raw_content).strip() != ""

                if already_generated:
                    html_content = raw_content
                else:
                    # 需要调用模型生成
                    with st.spinner("Generating..."):
                        try:
                            # 调用模型
                            html_content = model.generate_with_qwen(row['query'], system_prompt_1225)

                            # --- 关键：写入数据并保存 ---
                            # 1. 更新 DataFrame 内存数据
                            test_case.at[index, target_column_name] = html_content

                            # 2. 写入 CSV (每次生成完立即保存)
                            # 使用 utf-8-sig 防止中文乱码
                            test_case.to_csv(file_path, index=False, encoding='utf-8-sig')
                            # ---------------------------

                        except Exception as e:
                            st.error(f"生成失败: {e}")
                            html_content = ""

                # 3. 渲染组件 (安全检查)
                if html_content and isinstance(html_content, str) and html_content.strip() != "":
                    # 这里使用 components.html 渲染，高度固定 1000
                    components.html(html_content, height=1000, scrolling=True)

                # 4. 结尾
                if pd.notna(row.get('结尾1')):
                    st.markdown(row['结尾1'])

                # 5. 源码调试
                if html_content:
                    with st.expander("View Source Code"):
                        st.code(html_content, language='html')

        # 【速率限制逻辑】
        # 只有在真正调用了 API 生成（没有走缓存）时才休眠
        if not already_generated:
            time.sleep(60)