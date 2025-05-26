import gradio as gr
from PIL import Image
import random
import time
from openai import OpenAI
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
from io import BytesIO
client = OpenAI(api_key="", base_url="https://api.deepseek.com")


def generate_recipe(ingredients, preferences=""):
    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content":f"用以下食材生成一个有创意的食谱{ingredients},并为这道菜生成图片描述以便我通过文生图模型生成一张成品图,将两个部分用\'图片描述\'隔开"},
    ],
    stream=False
    )
    recipe,descirbe=response.choices[0].message.content.split("图片描述")
    return recipe,descirbe


def generate_food_image(prompt):
   

    rsp = ImageSynthesis.call(api_key="",
                            model="wanx2.1-t2i-turbo",
                            prompt=prompt,
                            n=1,
                            size='1024*1024')
    if rsp.status_code == HTTPStatus.OK:

        for result in rsp.output.results:

            with open('%s' % "picture.png", 'wb+') as f:
                f.write(requests.get(result.url).content)
    else:
        print('sync_call Failed, status_code: %s, code: %s, message: %s' %
                (rsp.status_code, rsp.code, rsp.message))
        
    return Image.open("picture.png")


def process_flow(ingredients, preferences):

    recipe,description= generate_recipe(ingredients, preferences)
    
    image = generate_food_image(description)
    # assert isinstance(Image, Image.Image), "必须返回PIL图像"
    # assert isinstance(recipe, str), "菜谱必须为字符串"
    # assert isinstance(description, str), "描述必须为字符串"
        
    return recipe,image

with gr.Blocks(title="AI食谱生成器", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🍳 AI智能食谱生成器")
    
    with gr.Row():
        with gr.Column(scale=1):
            ingredients_input = gr.Textbox(
                label="输入食材（多个用逗号分隔）",
                placeholder="例：牛肉, 土豆, 胡萝卜"
            )
            preferences_input = gr.Textbox(
                label="特殊要求（可选）",
                placeholder="例：少油少盐，西式风味"
            )
            submit_btn = gr.Button("生成菜谱", variant="primary")
        
        with gr.Column(scale=2):
            recipe_output = gr.Markdown(label="生成的菜谱")
            with gr.Row():
                # description_output = gr.Textbox(label="图片描述")
                image_output = gr.Image(label="菜品示意图",type="pil")


    submit_btn.click(
        fn=process_flow,
        inputs=[ingredients_input, preferences_input],
        outputs=[recipe_output,image_output]
    )

if __name__ == "__main__":

    demo.launch(share=True)
    # process_flow("","")
    # generate_food_image("食物")
    
