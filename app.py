import streamlit as st
import streamlit.components.v1 as components
import os
import glob
from datetime import datetime, timedelta
import model

# 页面配置
st.set_page_config(
    page_title="Prompt 测试工具",
    page_icon="🤖",
    layout="wide"
)

# ==============================================================================
# 频率限制配置
# ==============================================================================
MAX_REQUESTS_PER_HOUR = 10
RATE_LIMIT_WINDOW = timedelta(hours=1)

# 初始化 session state
if 'request_times' not in st.session_state:
    st.session_state['request_times'] = []

if 'generated_count' not in st.session_state:
    st.session_state['generated_count'] = 0


def check_rate_limit():
    """检查是否超过频率限制"""
    now = datetime.now()

    # 清理超过1小时的请求记录
    st.session_state['request_times'] = [
        t for t in st.session_state['request_times']
        if now - t < RATE_LIMIT_WINDOW
    ]

    # 检查是否超过限制
    if len(st.session_state['request_times']) >= MAX_REQUESTS_PER_HOUR:
        return False

    # 记录本次请求
    st.session_state['request_times'].append(now)
    st.session_state['generated_count'] += 1
    return True


def get_remaining_requests():
    """获取剩余请求次数"""
    now = datetime.now()
    st.session_state['request_times'] = [
        t for t in st.session_state['request_times']
        if now - t < RATE_LIMIT_WINDOW
    ]
    return max(0, MAX_REQUESTS_PER_HOUR - len(st.session_state['request_times']))


# ==============================================================================
# 内置 API 密钥（仅供内部测试使用）
# ==============================================================================
DEFAULT_OPENAI_API_KEY = "Zq2YTTh5DFGtdLpETX1zJ6J8cauCH8Cn"
DEFAULT_GEMINI_API_KEY = "AIzaSyCjLQYjGvp7g8dP55hYtjhszsPJ-6n8Dfs"

# ==============================================================================
# 侧边栏 - 配置区域
# ==============================================================================
st.sidebar.title("⚙️ 配置")

# API 密钥配置
st.sidebar.header("API 密钥")
api_provider = st.sidebar.selectbox(
    "选择模型提供商",
    ["Qwen (默认)", "Gemini"],
    help="选择要使用的 AI 模型"
)

api_key = ""
base_url = ""

if api_provider == "Qwen (默认)":
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        value=DEFAULT_OPENAI_API_KEY,
        help="用于调用 Qwen 模型"
    )
    base_url = st.sidebar.text_input(
        "API Base URL",
        value="https://antchat.alipay.com/v1",
        help="API 端点地址"
    )
    model_name = st.sidebar.text_input(
        "Model Name",
        value="Qwen3-235B-A22B-Instruct-2507"
    )
else:
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        value=DEFAULT_GEMINI_API_KEY,
        help="用于调用 Gemini 模型"
    )
    model_name = "gemini-2.5-flash"

# System Prompt 配置
st.sidebar.header("System Prompt")

# 获取 prompt 目录中的预设 prompt
prompt_dir = "/Users/shangguan/PycharmProjects/workbench/prompt"
prompt_files = glob.glob(os.path.join(prompt_dir, "*.md"))

# 构建选项列表
prompt_options = ["自定义输入"]
if prompt_files:
    for f in prompt_files:
        prompt_options.append(os.path.basename(f))

selected_prompt = st.sidebar.selectbox(
    "选择 System Prompt",
    prompt_options
)

system_prompt = ""

if selected_prompt == "自定义输入":
    system_prompt = st.sidebar.text_area(
        "输入自定义 System Prompt",
        height=200,
        help="输入您自己的系统提示词"
    )
elif selected_prompt:
    # 读取选中的 prompt 文件
    prompt_path = os.path.join(prompt_dir, selected_prompt)
    with open(prompt_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    st.sidebar.text_area(
        "当前 System Prompt 预览",
        value=system_prompt[:500] + "..." if len(system_prompt) > 500 else system_prompt,
        height=150,
        disabled=True
    )

# 频率限制显示
st.sidebar.header("使用限制")
remaining = get_remaining_requests()
st.sidebar.info(f"剩余生成次数: {remaining}/{MAX_REQUESTS_PER_HOUR} (每小时)")

# ==============================================================================
# 主界面
# ==============================================================================
st.title("🤖 Prompt 测试工具")
st.markdown("输入您的 Query，测试 AI 生成的回答效果")

# 用户输入区域
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 输入")
    user_query = st.text_area(
        "用户 Query",
        height=100,
        placeholder="请输入您要测试的问题..."
    )

    user_context = st.text_area(
        "上下文/RAG 参考资料 (可选)",
        height=100,
        placeholder="提供上下文或搜索结果..."
    )

    # 构造输入内容
    input_content = user_query
    if user_context:
        input_content = f"""
search_content: {user_context}
user_query: {user_query}
"""

    # 生成按钮
    generate_btn = st.button("🚀 生成回答", type="primary", disabled=remaining <= 0)

# ==============================================================================
# 生成与展示
# ==============================================================================
if generate_btn:
    if not user_query:
        st.error("请输入用户 Query")
    elif not system_prompt:
        st.error("请配置 System Prompt")
    elif not api_key:
        st.error("请输入 API 密钥")
    elif not check_rate_limit():
        st.error("已达到每小时生成次数上限，请稍后再试")
    else:
        with st.spinner("AI 正在生成回答..."):
            try:
                if api_provider == "Qwen (默认)":
                    html_content = model.generate_with_qwen(
                        input_content=input_content,
                        system_prompt=system_prompt,
                        api_key=api_key,
                        base_url=base_url,
                        model_name=model_name
                    )
                else:
                    html_content = model.generate_with_gemini(
                        input_content=input_content,
                        system_prompt=system_prompt,
                        api_key=api_key
                    )

                if html_content:
                    with col2:
                        st.subheader("📱 预览效果")

                        # 手机模拟器样式
                        phone_style = """
                        <style>
                        .phone-frame {
                            width: 375px;
                            height: 812px;
                            border: 12px solid #333;
                            border-radius: 40px;
                            overflow: hidden;
                            margin: 0 auto;
                            background: #fff;
                            position: relative;
                        }
                        .phone-notch {
                            width: 150px;
                            height: 30px;
                            background: #333;
                            position: absolute;
                            top: 0;
                            left: 50%;
                            transform: translateX(-50%);
                            border-bottom-left-radius: 15px;
                            border-bottom-right-radius: 15px;
                            z-index: 10;
                        }
                        .phone-content {
                            width: 100%;
                            height: 100%;
                            overflow-y: auto;
                            padding-top: 30px;
                        }
                        </style>
                        """

                        # 显示手机框架
                        st.markdown(phone_style, unsafe_allow_html=True)

                        # 渲染 HTML 内容
                        if html_content:
                            # 确保内容在手机模拟器中显示
                            scaled_html = f"""
                            <div style="transform: scale(0.5); transform-origin: top left; width: 200%; height: 200%;">
                                {html_content}
                            </div>
                            """
                            components.html(scaled_html, height=500, scrolling=True)

                        # 显示剩余次数
                        remaining = get_remaining_requests()
                        st.success(f"生成成功！剩余次数: {remaining}/{MAX_REQUESTS_PER_HOUR}")

                    # HTML 源码展示
                    with st.expander("📄 查看/复制 HTML 源码"):
                        st.code(html_content, language='html')
                else:
                    st.error("生成失败，请检查 API 密钥和网络连接")

            except Exception as e:
                st.error(f"生成出错: {str(e)}")

# ==============================================================================
# 使用说明
# ==============================================================================
with st.expander("📖 使用说明"):
    st.markdown("""
    **使用流程：**

    1. **配置 API 密钥**：在左侧边栏选择模型提供商并输入 API 密钥
    2. **选择 System Prompt**：从预设列表选择或自定义输入
    3. **输入 Query**：在主界面输入用户问题和上下文
    4. **生成预览**：点击生成按钮，查看手机模拟器中的效果

    **频率限制**：每小时最多生成 10 次

    **提示**：如果使用自定义 API 端点，请确保 Base URL 正确
    """)