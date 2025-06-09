from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from utils.generate_recipe import generate_recipe
from utils.generate_image_description import generate_image_description
from utils.generate_dish_image import generate_dish_image
from utils.generate_steps_image import generate_steps_image
from utils.generate_nutritional_analysis import generate_nutrition_analysis
from utils.class_login import login
from PIL import Image
import os
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 设置会话密钥

@app.route('/')
def home():
    # 检查用户是否已登录
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    action = request.form.get('action')  # 'login' 或 'register'
    
    login_manager = login()
    
    if action == 'login':
        if login_manager.authenticate(username, password):
            session['username'] = username
            return jsonify({'success': True, 'message': '登录成功'})
        return jsonify({'success': False, 'message': '用户名或密码错误'})
    
    elif action == 'register':
        if login_manager.register(username, password):
            session['username'] = username
            return jsonify({'success': True, 'message': '注册成功'})
        return jsonify({'success': False, 'message': '用户名已存在'})
    
    return jsonify({'success': False, 'message': '无效操作'})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html', username=session['username'])

@app.route('/generate', methods=['POST'])
def generate():
    if 'username' not in session:
        return jsonify({"error": "未登录"}), 401
        
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