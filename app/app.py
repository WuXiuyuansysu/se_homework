from flask import Flask, render_template, request, jsonify
from utils.generate_recipe import generate_recipe
from utils.generate_image_description import generate_image_description
from utils.generate_dish_image import generate_dish_image
from utils.generate_steps_image import generate_steps_image
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
        recipe = generate_recipe(
            ingredients=ingredients,
            cuisine_type=cuisine_type
        )
        
        """
        generate_steps_image返回list, 其每个元素是一个Image对象, 图像内容某个做菜的步骤
        generate_image_description返回json, 内容是对最终菜肴图像生成的建议
        generate_dish_image返回Image对象,图像内容是最终菜肴的图像

        所有的图片都保存在 ./pictures下面:
            步骤图片命名为1.png...(前缀取决于recipe[steps][item][step]的内容）
            最终菜肴命名为dish_image.png

        test.py中运行了所有后端的流程
        每个函数对应的文件下面设置了对应的测试代码
        请根据后端函数返回值更改generate()的返回值以适应前端需求
        """
        steps_img = generate_steps_image(recipe)
        dish_desciption = generate_image_description(recipe)
        dish_img = generate_dish_image(dish_desciption)
        
        
        return jsonify({
            "recipe": recipe,
            
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)