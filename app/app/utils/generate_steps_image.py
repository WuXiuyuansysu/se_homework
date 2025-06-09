from PIL import Image
import requests
from dashscope import ImageSynthesis
import os
import openai
from openai import OpenAI
import json
import re

def get_recipe_steps_description(recipe):
    steps_description = list()
    for item in recipe['steps']:
        steps_description.append((item['step'], item['description']))
    return steps_description

def generate_steps_image(recipe):
    """每个做菜步骤的图片"""

    steps_description = get_recipe_steps_description(recipe)
    step_imgs = list()
    for step_description in steps_description:
        prompt = step_description[1]
        rsp = ImageSynthesis.call(api_key="sk-b8e09876066e40aab6ee92ba4a12629b",
                        model="wanx2.1-t2i-turbo",
                        prompt=prompt,
                        n=1,
                        size='1024*1024')

        result = rsp.output.results[0]

        output_dir = r"./pictures"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        image_path = os.path.join(output_dir, f"{step_description[0]}.png")
        with open(image_path, 'wb') as f:
            f.write(requests.get(result.url).content)

        step_imgs.append(Image.open(image_path))

    return step_imgs
    
if __name__ == "__main__":
    test_recipe = {
        "steps": [
            {
                "step": "step1",
                "description": "将土豆切成薄片，放入水中浸泡10分钟以去除多余淀粉。"
            },
            {
                "step": "step2",
                "description": "将洋葱切成细丝，胡萝卜切成薄片。"
            },
            {
                "step": "step3",
                "description": "在锅中加入橄榄油，加热至中火，放入洋葱丝炒至透明。"
            },
            {
                "step": "step4",
                "description": "加入胡萝卜片，继续翻炒3分钟。"
            },
            {
                "step": "step5",
                "description": "将土豆片沥干水分，加入锅中，翻炒均匀。"
            },
            {
                "step": "step6",
                "description": "加入适量盐和黑胡椒调味，炒至土豆片变软。"
            }
        ]
    }
    generate_steps_image(test_recipe)