from flask import Flask, render_template, request, jsonify
from utils.generate_recipe import generate_recipe
from utils.generate_image_description import generate_image_description
from utils.generate_dish_image import generate_dish_image
from utils.generate_steps_image import generate_steps_image
from utils.generate_nutritional_analysis import generate_nutrition_analysis
from PIL import Image
import requests
import os

import base64
from io import BytesIO

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = 'static/images'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    ingredients = request.form.get('ingredients')
    cuisine_type = request.form.get('cuisine_type')
    
    try:
        recipe = generate_recipe(
            ingredients=ingredients,
            cuisine_type=cuisine_type
        )
        

        # 生成菜品外貌描述
        appearance_desc = generate_image_description(recipe)
        img = generate_dish_image(appearance_desc)
        # 将图片转换为base64编码
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        dish_nutrition=generate_nutrition_analysis(recipe)
        # 生成每个步骤的图片描述
        step_imgs = generate_steps_image(recipe)
        
        step_base64 = []
        for image in step_imgs:
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            step_base64.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))

        
        # 返回组合数据
        return jsonify({
            "recipe": recipe,
            "steps_images": step_base64,
            "dish_image": img_base64, 
            "nutrition": dish_nutrition 

        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
