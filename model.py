from google import genai
import os
from google.genai import types
from openai import OpenAI

# define model name
model_name = [
    "gemini-2.5-flash",
    "gemini-3-pro-preview"
]

# API 配置 - 从环境变量读取，支持用户自定义
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://antchat.alipay.com/v1")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "Qwen3-235B-A22B-Instruct-2507")

# Gemini 配置 - 从环境变量读取
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_PROXY = os.environ.get("GEMINI_PROXY", "")


def get_gemini_client(api_key=None):
    """
    初始化并返回 gemini_client
    """
    key = api_key or GEMINI_API_KEY
    if not key:
        raise ValueError("Gemini API key is required. Please set GEMINI_API_KEY environment variable or provide it in the UI.")

    # 设置代理（如果配置了）
    if GEMINI_PROXY:
        os.environ['HTTP_PROXY'] = GEMINI_PROXY
        os.environ['HTTPS_PROXY'] = GEMINI_PROXY
        os.environ['ALL_PROXY'] = GEMINI_PROXY

    return genai.Client(api_key=key)

def generate_with_gemini(input_content, system_prompt, api_key=None):
    client = get_gemini_client(api_key)
    response = client.models.generate_content(
        model=model_name[0],
        contents=input_content,
        config=types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=system_prompt
        )
    )
    return response.text


def get_qwen_client(api_key=None, base_url=None):
    """
    初始化并返回 OpenAI client (用于调用 Qwen)
    """
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY environment variable or provide it in the UI.")

    url = base_url or OPENAI_BASE_URL

    return OpenAI(
        api_key=key,
        base_url=url
    )



def generate_with_qwen(input_content, system_prompt, api_key=None, base_url=None, model_name=None):
    """
    使用 OpenAI 兼容接口调用 Qwen 模型
    """
    client = get_qwen_client(api_key, base_url)

    try:
        response = client.chat.completions.create(
            model=model_name or DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_content}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error calling Qwen: {e}")
        return None



# 测试调用 (可选)
if __name__ == "__main__":
    res = generate_with_qwen("搜索结果", "用户上下文", "你好", "你是一个助手")
    print(res)