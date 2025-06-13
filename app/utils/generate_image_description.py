import openai
from openai import OpenAI  # 明确导入OpenAI类
import json
import re


def generate_image_description(recipe):
    """
    根据菜谱信息生成菜品外观的详细描述。

    参数:
        recipe (dict): 包含菜谱内容的字典，必须包含以下字段：
            - 'name': 菜谱名称（字符串）
            - 'ingredients': 食材列表，每个元素是包含 'name' 和 'quantity' 的字典
            - 'steps': 制作步骤列表，每个元素为包含 'description' 的字典
            - 'total_time': 总烹饪时间（字符串）

    功能:
        - 构建专业提示词，基于菜谱名称、食材、关键步骤和时间生成详细描述；
        - 调用 AI 接口生成关于菜品视觉外貌的 JSON 格式描述，包括摆盘、食材外观、酱汁光泽和摄影建议；
        - 返回一个 JSON 对象（Python 字典格式），可用于图像生成提示。

    返回:
        dict: 包含以下字段的 JSON 对象：
            - 'style': 摆盘风格描述
            - 'ingredients_visual': 主要食材的视觉效果
            - 'sauce_gloss': 酱汁或汤汁的光泽表现
            - 'photography_tips': 拍摄建议

    注意:
        输出 JSON 格式严格受限，必须满足接口返回的规范。
    """
    
    prompt = f"""
        你是一个专业美食摄影师，需要根据以下菜谱生成菜品外观的详细描述。
        请严格按照以下规则输出：

        ----- 规则 -----
        1. 输出必须是纯净的 JSON 对象，不要包含任何注释、Markdown、XML/HTML 或其他非 JSON 内容。
        2. JSON 必须包含以下字段：
        - "style": 描述整体摆盘风格（如圆形、对称、现代极简）。
        - "ingredients_visual": 基于菜谱中的食材列表，描述主要食材的视觉呈现方式（如颜色对比、分层效果）。
        - "sauce_gloss": 酱汁或汤汁的光泽度（如镜面反光、哑光质地）。
        - "photography_tips": 拍摄建议（如 45 度俯拍、逆光柔光）。
        3. 必须基于菜谱的以下信息生成内容：
        - 菜谱名称：{recipe['name']}
        - 使用食材：{', '.join([f"{ing['name']}（{ing['quantity']}）" for ing in recipe['ingredients']])}
        - 关键步骤：{recipe['steps'][0]['description']}（第一步）, {recipe['steps'][-1]['description']}（最后一步）
        - 总烹饪时间：{recipe['total_time']}（影响菜品完成状态）

        ----- 示例 -----
        正确输出格式示例：
        {{
            "style": "现代极简主义摆盘，中央主食材堆叠，周围留白",
            "ingredients_visual": "鲜红番茄片与嫩黄炒蛋形成色彩对比，葱花点缀",
            "sauce_gloss": "金黄色蛋液包裹食材，呈现丝绸般光泽",
            "photography_tips": "建议使用 45 度俯拍，搭配侧逆光突出层次感"
        }}"""
    
    client = OpenAI(
        api_key="sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo",
        base_url="https://api.suanli.cn/v1"
    )
    
    response = client.chat.completions.create(
        model="free:Qwen3-30B-A3B",
        messages=[
            {"role": "system", "content": "你是一个专业摄影师，输出必须是纯净的 JSON 对象，不要任何额外文本"},
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
        description = generate_image_description(recipe_example)
        print("生成的菜品描述:")
        print(description)
    except Exception as e:
        print(f"调用失败: {e}")