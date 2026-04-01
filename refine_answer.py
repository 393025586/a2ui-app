import pandas as pd
import time
import model  # 保持你原有的model模块
from datetime import datetime
import os
from google.genai import types

# --- 配置区域 ---
# 注意：文件名后缀是 .xlsx，请确保安装了 openpyxl (pip install openpyxl)
FILE_PATH = "/Users/shangguan/PycharmProjects/workbench/data_files/10goodcase.csv"
PROMPT_PATH = '/Users/shangguan/PycharmProjects/workbench/prompt/sp_CSS_with_search.md'
SLEEP_SECONDS = 5  # API 调用间隔


def load_data():
    """加载数据，根据扩展名自动选择读取方式"""
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(f"文件不存在: {FILE_PATH}")

    # 根据后缀判断读取方式
    if FILE_PATH.endswith('.xlsx'):
        df = pd.read_excel(FILE_PATH)
    else:
        df = pd.read_csv(FILE_PATH)

    # 按照截图中的列名 'query' 去除空行
    # 注意：确保Excel里列名没有多余空格
    df = df.dropna(subset=['query'])
    return df


# ==============================================================================
# 2. 确定目标列名
# ==============================================================================
def determine_target_column(df):
    """
    智能确定要填充的目标列
    """
    existing_cols = [c for c in df.columns if str(c).startswith("8部分内容_")]

    if existing_cols:
        last_col = existing_cols[-1]
        # 检查是否全部非空且不为空字符串
        is_complete = df[last_col].apply(
            lambda x: pd.notna(x) and str(x).strip() != ""
        ).all()

        if not is_complete:
            print(f"检测到未完成任务，继续填充: {last_col}")
            return last_col, df

    timestamp = datetime.now().strftime("%m%d_%H%M")
    new_col = f"8部分内容_{timestamp}"
    df[new_col] = ""
    print(f"创建新任务列: {new_col}")

    return new_col, df


# ==============================================================================
# 3. 加载 Prompt
# ==============================================================================
def load_prompt():
    if not os.path.exists(PROMPT_PATH):
        raise FileNotFoundError(f"Prompt文件找不到: {PROMPT_PATH}")

    with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
        return f.read()


# ==============================================================================
# 4. 批量生成 (核心修改部分)
# ==============================================================================
def generate_all_html(df, target_col, system_prompt):
    total_rows = len(df)

    # 统计待生成数量
    to_generate = df[target_col].apply(
        lambda x: not (pd.notna(x) and str(x).strip() != "")
    ).sum()

    generated_count = 0
    client = model.get_gemini_client()

    print(f"开始任务，共需生成 {to_generate} 条数据...")

    for index, row in df.iterrows():
        # 1. 检查是否已生成
        existing_content = row.get(target_col)
        if pd.notna(existing_content) and str(existing_content).strip() != "":
            # print(f"Row {index + 1}: 跳过") # 减少刷屏，可注释
            continue

        # 2. 提取数据 (对应截图中的列名)
        query = str(row['query']) if pd.notna(row['query']) else ""

        # 提取上下文，如果是 NaN 则留空
        pre_1 = str(row['前1']) if pd.notna(row['前1']) else "无"
        mid_8 = str(row['中间8']) if pd.notna(row['中间8']) else "无"
        post_1 = str(row['后1']) if pd.notna(row['后1']) else "无"
        advice = str(row['修改意见']) if pd.notna(row['修改意见']) else "无"

        # 3. 组装 Prompt (综合参考逻辑)
        input_content = f"""
                请根据以下参考信息（前言、中间内容、结尾）以及修改意见，对用户的提问(Query)做出最终回答。

                【用户提问 (Query)】: 
                {query}

                【参考上下文 - 开头 (Part 1)】:
                {pre_1}

                【参考上下文 - 中间部分 (Part 2)】:
                {mid_8}

                【参考上下文 - 结尾 (Part 3)】:
                {post_1}

                【修改意见 (Instructions)】:
                {advice}

                任务目标：
                请综合上述“参考上下文”的内容，并严格遵循“修改意见”，重新生成“中间部分”。注意你生成的不是完整回答，是中间8，所以请不要出现和开头1、结尾1重复的内容。
                当中间8部分有给到参考时，请严格参考，不要过多修改，仅修改Instructions提到的内容
                """

        print(f"Row {index + 1}/{total_rows} 正在生成: {query[:30]}...")

        try:
            # 配置 Google Search 和 System Prompt
            tool_config = types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                system_instruction=system_prompt
            )

            # 创建对话
            chat = client.chats.create(
                model=model.model_name[0],
                config=tool_config
            )

            response = chat.send_message(input_content)

            # 获取文本结果
            result_content = response.text

            # 写入 DataFrame
            df.at[index, target_col] = result_content

            # 立即保存 (使用 Excel 格式保存)
            if FILE_PATH.endswith('.xlsx'):
                df.to_excel(FILE_PATH, index=False)
            else:
                df.to_csv(FILE_PATH, index=False, encoding='utf-8-sig')

            generated_count += 1
            print(f"✅ 生成成功 ({generated_count}/{to_generate})")

            # 速率限制
            if generated_count < to_generate:
                print(f"⏳ 等待 {SLEEP_SECONDS} 秒...")
                time.sleep(SLEEP_SECONDS)

        except Exception as e:
            print(f"❌ 生成失败 Row {index}: {e}")
            # 可以选择不记录错误信息，方便下次重跑，或者记录 ERROR
            df.at[index, target_col] = f"ERROR: {str(e)}"
            # 出错也保存一下
            if FILE_PATH.endswith('.xlsx'):
                df.to_excel(FILE_PATH, index=False)
            else:
                df.to_csv(FILE_PATH, index=False, encoding='utf-8-sig')

    return df


# ==============================================================================
# 5. 主函数
# ==============================================================================
def main():
    try:
        # 1. 加载数据
        df = load_data()

        # 2. 确定列
        target_col, df = determine_target_column(df)

        # 3. 加载 Prompt
        system_prompt = load_prompt()

        # 4. 执行生成
        df = generate_all_html(df, target_col, system_prompt)

        print("\n🎉 所有任务已完成")

    except Exception as e:
        print(f"\n程序异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()