from flask import Flask, render_template, request, jsonify
from utils.generate_recipe import generate_recipe
import base64

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
        # 生成菜谱
        recipe = generate_recipe(
            ingredients=ingredients,
            cuisine_type=cuisine_type
        )
        
        # 生成菜品外貌描述
        #appearance_desc = generate_image_description(recipe)
        
        # 生成图片并保存为Base64
        #image_data = generate_dish_image(appearance_desc)
        #image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # 返回组合数据
        return jsonify(recipe)  # 改为返回JSON数据
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)