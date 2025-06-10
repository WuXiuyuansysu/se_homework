import openai
from openai import OpenAI  # 明确导入OpenAI类
import json
import re

def generate_prefer_recipe(preferences):
    """食谱"""

    prompt = f"""
    请根据以下用户喜好生成详细的菜谱，严格遵守以下要求：
    1. 输出必须是纯净的JSON对象，禁止包含任何其他文本、注释、XML/HTML标签或Markdown代码块
    2. 确保JSON的语法正确性，包括引号、逗号和大括号匹配
    3. 直接以JSON对象开头，不要有其他前缀
    4. 每种食材和调料都精确到克

    {preferences}

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
        api_key="sk-b8e09876066e40aab6ee92ba4a12629b",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    
    completion = client.chat.completions.create(
        model="qwen-plus", 
        messages=[
            {'role': 'system', 'content': 'You are a very skilled chef.'},
            {'role': 'user', 'content': prompt}
            ]
    )
    json_content = json.loads(completion.choices[0].message.content)

    return json_content

if __name__ == "__main__":
    ingredients = "鸭腿，洋葱，米饭，牛排，西兰花"
    cuisine_type = "中式粤菜"
    print(generate_prefer_recipe(
        ingredients=ingredients,
        cuisine_type=cuisine_type
    ))

