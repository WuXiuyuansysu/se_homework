import openai
from openai import OpenAI  # 明确导入OpenAI类
import json
import re

def generate_image_description(recipe):
    """生成菜品外貌描述"""
    prompt = f"""
    严格遵守以下要求：
    1. 输出必须是纯净的JSON对象，禁止包含任何其他文本、注释、XML/HTML标签或Markdown代码块
    2. 确保JSON的语法正确性，包括引号、逗号和大括号匹配
    3. 直接以JSON对象开头，不要有其他前缀
    根据以下菜谱生成菜品外观的专业摄影描述，包含以下要素：
    1. 菜品整体摆盘风格
    2. 主要食材的视觉呈现方式
    3. 酱汁/汤汁的光泽度描述
    4. 建议拍摄角度和光影效果
    
    菜谱名称：{recipe['name']}
    烹饪方式：{recipe['steps']}
    输出要求：直接返回纯文本描述，不要任何格式"""
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