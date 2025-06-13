import openai
from openai import OpenAI  # 明确导入OpenAI类
import json
import re

def generate_recipe(ingredients, cuisine_type):
    """
    根据指定食材与菜系类型生成标准化菜谱。

    参数:
        ingredients (str): 食材列表（文本格式），例如："鸡胸肉200克，胡萝卜100克，洋葱1个"
        cuisine_type (str): 菜系风格，例如："川菜"、"意大利菜"、"粤菜"

    功能:
        - 构造提示词，通过大语言模型生成符合指定食材与菜系风格的完整菜谱；
        - 输出为纯净、符合语法要求的 JSON 格式，结构标准，适用于进一步处理或前端展示；
        - 每种食材和调料都要求精确计量（单位为克），步骤包含描述与耗时。

    返回:
        dict: 菜谱信息的 JSON 对象，格式如下：
            - "name" (str): 菜谱名称；
            - "ingredients" (list): 食材列表，元素为：
                - "name" (str): 食材名称；
                - "quantity" (str): 食材用量（如 "150克"）；
            - "steps" (list): 烹饪步骤，元素为：
                - "step" (int): 步骤编号；
                - "description" (str): 步骤说明；
                - "duration" (str): 所需时间（如 "5分钟"）；
            - "total_time" (str): 总烹饪时间（如 "30分钟"）

    注意事项:
        - 输出内容依赖外部语言模型，建议在上层逻辑中增加格式与字段合法性校验；
        - 若返回格式错误或为空，应加入异常处理机制，避免程序崩溃。
    """

    prompt = f"""
    请根据以下食材和烹饪风格生成详细的菜谱，严格遵守以下要求：
    1. 输出必须是纯净的JSON对象，禁止包含任何其他文本、注释、XML/HTML标签或Markdown代码块
    2. 确保JSON的语法正确性，包括引号、逗号和大括号匹配
    3. 直接以JSON对象开头，不要有其他前缀
    4. 每种食材和调料都精确到克
    5. 明显无法食用的食材需要在结果中标注（如原子弹，大便等）

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
    print(generate_recipe(
        ingredients=ingredients,
        cuisine_type=cuisine_type
    ))

