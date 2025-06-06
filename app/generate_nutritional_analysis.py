import openai
from openai import OpenAI
import json

def generate_nutrition_analysis(recipe):
    """生成菜谱营养分析"""
    
    prompt = f"""
        你是一个专业营养师，需要根据以下菜谱生成详细的营养分析。
        请严格按照以下规则输出：

        ----- 规则 -----
        1. 输出必须是纯净的 JSON 对象，不要包含任何注释、Markdown、XML/HTML 或其他非 JSON 内容。
        2. JSON 必须包含以下字段：
        - "calories": 估算总卡路里（千卡）
        - "protein": 蛋白质含量（克）
        - "fat": 脂肪含量（克）
        - "carbohydrates": 碳水化合物含量（克）
        - "dietary_fiber": 膳食纤维含量（克）可选，如果无法计算可以省略
        - "key_nutrients": 一个数组，列出2-4种关键营养素（如维生素C、钙）及其含量和单位（如毫克、微克）和主要来源食材
        3. 必须基于菜谱的以下信息生成内容：
        - 菜谱名称：{recipe['name']}
        - 使用食材：{', '.join([f"{ing['name']}（{ing['quantity']}）" for ing in recipe['ingredients']])}
        - 烹饪方法：{recipe['steps'][0]['description']}（第一步）, {recipe['steps'][-1]['description']}（最后一步）
        - 份量信息：根据食材总量合理估算

        ----- 示例 -----
        正确输出格式示例：
        {{
            "calories": 450,
            "protein": 18,
            "fat": 15,
            "carbohydrates": 60,
            "dietary_fiber": 5,
            "key_nutrients": [
                {{"nutrient": "维生素C", "amount": 25, "unit": "毫克", "source": "番茄"}},
                {{"nutrient": "钙", "amount": 200, "unit": "毫克", "source": "奶酪"}}
            ]
        }}"""
    
    client = OpenAI(
        api_key="sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo",
        base_url="https://api.suanli.cn/v1"
    )
    
    response = client.chat.completions.create(
        model="free:Qwen3-30B-A3B",
        messages=[
            {"role": "system", "content": "你是一个专业营养师，输出必须是纯净的 JSON 对象，不要任何额外文本"},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}  # 强制 JSON 格式
    )
    json_content = json.loads(response.choices[0].message.content)
    
    return json_content

if __name__ == "__main__":
    recipe_example = {
        "name": "经典意大利面",
        "ingredients": [
            {"name": "意大利面", "quantity": "200克"},
            {"name": "橄榄油", "quantity": "2汤匙"},
            {"name": "大蒜", "quantity": "3瓣"},
            {"name": "番茄酱", "quantity": "150克"},
            {"name": "盐", "quantity": "适量"},
            {"name": "黑胡椒", "quantity": "适量"},
            {"name": "罗勒叶", "quantity": "适量"}
        ],
        "steps": [
            {"step": 1, "description": "煮沸一锅盐水，放入意大利面煮约8-10分钟至熟", "duration": "10分钟"},
            {"step": 2, "description": "锅中加热橄榄油，爆香切片大蒜", "duration": "2分钟"},
            {"step": 3, "description": "加入番茄酱煮沸，调入盐和黑胡椒", "duration": "5分钟"},
            {"step": 4, "description": "将煮熟的意大利面沥水后加入锅中拌匀", "duration": "1分钟"},
            {"step": 5, "description": "撒上新鲜罗勒叶装饰，盛盘", "duration": "1分钟"}
        ],
        "total_time": "20分钟"
    }

    try:
        nutrition = generate_nutrition_analysis(recipe_example)
        print("生成的营养分析:")
        print(json.dumps(nutrition, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"调用失败: {e}")
