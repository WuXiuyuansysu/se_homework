import openai
from openai import OpenAI  # 明确导入OpenAI类
import json
import re

def generate_recipe(ingredients, cuisine_type):
    prompt = f"""
    请根据以下食材和烹饪风格生成详细的菜谱，严格遵守以下要求：
    1. 输出必须是纯净的JSON对象，禁止包含任何其他文本、注释、XML/HTML标签或Markdown代码块
    2. 确保JSON的语法正确性，包括引号、逗号和大括号匹配
    3. 直接以JSON对象开头，不要有其他前缀
    4. 每种食材和调料都精确到克

    食材：{ingredients}
    菜式：{cuisine_type}

    示例格式：
    {{
        "name": "菜谱名称",
        "ingredients": [
            {{"name": "材料1", "quantity": "137克"}},
            ...
        ],
        "steps": [
            {{"step": 1, "description": "...", "duration": "5分钟"}},
            ...
        ],
        "total_time": "40分钟"
    }}"""

    client = OpenAI(
        api_key="sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo",
        base_url="https://api.suanli.cn/v1",
    )
    
    try:
        response = client.chat.completions.create(
            model="free:Qwen3-30B-A3B",
            messages=[{"role": "user", "content": prompt}]
        )
        raw_content = response.choices[0].message.content
        
        # 清理响应内容
        cleaned_content = raw_content.strip()
        cleaned_content = re.sub(r'<think>.*?</think>', '', cleaned_content, flags=re.DOTALL)
        cleaned_content = cleaned_content.replace('```json', '').replace('```', '').strip()
        
        # 提取JSON部分
        json_match = re.search(r'\{.*\}', cleaned_content, re.DOTALL)
        if not json_match:
            raise ValueError("API响应中未找到有效JSON内容")
        
        return json.loads(json_match.group())
        
    except json.JSONDecodeError as e:
        print("JSON解析失败，清理后的内容：", cleaned_content)
        raise ValueError("API返回的内容不符合JSON格式") from e
