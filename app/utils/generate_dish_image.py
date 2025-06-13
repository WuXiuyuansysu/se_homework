from PIL import Image
import requests
from dashscope import ImageSynthesis
import os

def generate_dish_image(description):
    """
    根据描述生成一张逼真的菜肴图片。

    参数:
        description (dict): 包含菜肴图像生成提示的字典，字段包括：
            - 'style': 装盘风格描述
            - 'ingredients_visual': 食材外观细节
            - 'sauce_gloss': 酱汁的光泽表现
            - 'photography_tips': 摄影技巧建议（如打光、构图）

    功能:
        - 构造一段详细的 food photography 提示词；
        - 调用图像合成模型生成图片；
        - 将生成的图像保存至本地 ./pictures/dish_image.png；
        - 返回生成的 PIL.Image 图像对象。

    返回:
        PIL.Image.Image: 菜肴图片的对象，可用于展示或进一步处理。
    """
    
    prompt = f"""
    根据以下食物摄影描述生成一张逼真的菜肴图片：
    1. 装盘风格：{description.get('style')}
    2. 食材外观：{description.get('ingredients_visual')}
    3. 酱汁光泽：{description.get('sauce_gloss')}
    4. 摄影技巧：{description.get('photography_tips')}
    
    其他要求：
    - 4K超高分辨率
    - 专业食物摄影风格
    - 浅景深突出主体
    - 自然光
    """

    rsp = ImageSynthesis.call(api_key="sk-b8e09876066e40aab6ee92ba4a12629b",
                            model="wanx2.1-t2i-turbo",
                            prompt=prompt,
                            n=1,
                            size='1024*1024')

    result = rsp.output.results[0]

    output_dir = r"./pictures"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_path = os.path.join(output_dir, "dish_image.png")
    with open(image_path, 'wb') as f:
        f.write(requests.get(result.url).content)

    return Image.open(image_path)

if __name__ == "__main__":
    test_description = {
        "style": "复古乡村风格，食材自然摆放，周围装饰着绿色植物",
        "ingredients_visual": "绿色菠菜与白色蘑菇搭配，点缀着红色樱桃番茄",
        "sauce_gloss": "透明的橄榄油轻轻覆盖在食材上，呈现出自然的光泽",
        "photography_tips": "正上方俯拍，均匀的自然光以突出食材的层次"
    }

    dish_image = generate_dish_image(test_description)

