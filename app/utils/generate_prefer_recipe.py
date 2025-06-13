import openai
from openai import OpenAI  # 明确导入OpenAI类
import json
import re

def generate_prefer_recipe(preferences):
    """
    根据用户偏好生成详细的菜谱。

    参数:
        preferences (str): 用户饮食偏好描述，例如口味、忌口、喜好食材、饮食限制等信息。
                          示例：'我喜欢川菜，偏辣，忌口花生和海鲜，希望总时间不超过30分钟。'

    功能:
        - 构造自然语言提示，向语言模型请求生成符合用户偏好的菜谱；
        - 返回标准化的菜谱 JSON 数据，包括名称、食材（单位为克）、步骤（带时间）、总耗时；
        - 要求模型返回纯净的 JSON 格式，禁止包含多余文本或格式错误。

    返回:
        dict: 菜谱信息的字典，包含以下字段：
            - "name" (str): 菜谱名称；
            - "ingredients" (list): 食材列表，每个元素为字典，包含：
                - "name": 食材名称；
                - "quantity": 食材用量（单位为克）；
            - "steps" (list): 步骤列表，每个元素为字典，包含：
                - "step": 步骤编号；
                - "description": 步骤说明；
                - "duration": 所需时间（例如"5分钟"）；
            - "total_time" (str): 总耗时（如"30分钟"）。

    注意:
        - 返回内容完全依赖语言模型，建议在上层增加校验逻辑；
        - 若生成失败或格式异常，应添加异常处理以保障系统稳定性。
    """

    prompt = f"""
    请根据以下食材和烹饪风格以及用户喜好生成详细的菜谱，严格遵守以下要求：
    1. 输出必须是纯净的JSON对象，禁止包含任何其他文本、注释、XML/HTML标签或Markdown代码块
    2. 确保JSON的语法正确性，包括引号、逗号和大括号匹配
    3. 直接以JSON对象开头，不要有其他前缀
    4. 每种食材和调料都精确到克
    5. 明显无法食用的食材需要在结果中标注（如原子弹，大便等）

    食材：{ingredients}
    菜式：{cuisine_type}
    用户喜好: {preferences}

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
        "dangerous_ingredients": ["成分1", "成分2"],
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

