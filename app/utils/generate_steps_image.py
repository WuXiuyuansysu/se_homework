from PIL import Image
import requests
from dashscope import ImageSynthesis
import os
import openai
from openai import OpenAI
import json
import re
import config
def get_recipe_steps_description(recipe):
    """
    从菜谱中提取每个步骤的编号和描述。

    参数：
        recipe (dict): 包含菜谱信息的字典，必须含有' steps'键，其值为步骤列表，每个步骤为字典，
                       其中包含' step'（步骤编号）和'description'（步骤描述）字段。

    返回：
        list of tuple: 返回一个列表，列表元素为元组(step编号, step描述)，
                       按照菜谱中步骤顺序排列。
    """
    steps_description = list()
    for item in recipe['steps']:
        steps_description.append((item['step'], item['description']))
    return steps_description

def generate_steps_image(recipe):
    """
    根据菜谱的每个烹饪步骤描述生成对应的图片列表。

    参数：
        recipe (dict): 菜谱信息，包含步骤描述，结构应包含步骤文本，可通过 get_recipe_steps_description() 函数获取步骤列表。

    功能：
        - 调用图像生成接口，根据每个步骤的文字描述生成对应的图片；
        - 图片统一保存到本地 ./pictures 目录，文件名为步骤标识（如步骤编号）；
        - 返回包含每步生成的PIL.Image对象的列表，顺序对应步骤顺序。

    返回：
        list[PIL.Image.Image]: 由步骤图片组成的列表，列表元素为每个步骤生成的PIL图片对象。

    注意事项：
        - 依赖外部函数 get_recipe_steps_description(recipe) 返回 [(步骤标识, 描述), ...] 格式的数据；
        - 需保证网络可用以调用图像接口并下载图片；
        - 图片保存路径固定为 ./pictures，可根据需求修改；
        - 若生成失败或网络异常，建议在调用端增加异常处理。
    """

    steps_description = get_recipe_steps_description(recipe)
    step_imgs = list()
    for step_description in steps_description:
        prompt = step_description[1]
        rsp = ImageSynthesis.call(api_key=config.API_KEY_0,
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