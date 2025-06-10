from math import log
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from classes.class_login import login
from classes.RecipeGenerationPipeline import RecipeGenerationPipeline
from classes.class_user import User
from classes.class_recipe import Recipe
from classes.class_login import login
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 设置会话密钥
    
login_manager = login()

# 初始化用户
@app.route('/')
def home():
    # 检查用户是否已登录
    if 'username' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login_page'))

# 登录页面
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# 登录或注册处理
@app.route('/login', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    action = request.form.get('action')  # 'login' 或 'register'

    
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

# 登出处理
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

# 首页
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html', username=session['username'])

# 生成食谱
@app.route('/generate', methods=['POST'])
def generate():
    if 'username' not in session:
        return jsonify({"error": "未登录"}), 401
        
    ingredients = request.form.get('ingredients')
    cuisine_type = request.form.get('cuisine_type')

    pipline = RecipeGenerationPipeline(ingredients, cuisine_type)
    result = pipline.execute()
        

    #保存历史记录
    user = User(session['username'])
    trans_data = {
        "name": result.name,
        "recipe": result.recipe,
        "steps_images": result.steps_imgs,
        "dish_image": result.total_img,
        "nutrition": result.dish_nutrition,
        "uml_sequence": result.uml_sequence
    }
    if user:
        user.save_recipe_to_history(result)
    else:
        return jsonify({"error": "用户不存在"}), 404
    
    return jsonify(trans_data)

# 用户个人资料页面
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    username = session['username']
    user = User(username)
    
    # 获取收藏和历史记录的菜谱列表
    likes_recipes = user.load_user_likes()
    history_recipes = user.load_user_history()
    
    return render_template(
        'profile.html', 
        username=username,
        likes=likes_recipes,
        history=history_recipes
    )

# 加载菜谱
@app.route('/load_recipe', methods=['GET'])
def load_recipe():
    if 'username' not in session:
        return jsonify({"error": "未登录"}), 401
        
    recipe_type = request.args.get('type')  # 'likes' 或 'history'
    filename = request.args.get('filename')
    
    if not recipe_type or not filename:
        return jsonify({"error": "参数缺失"}), 400
        
    username = session['username']
    user = User(username)
    
    # 根据类型加载菜谱
    if recipe_type == 'likes':
        recipe = user.load_recipe_from_likes(filename)
    elif recipe_type == 'history':
        recipe = user.load_recipe_from_history(filename)
    else:
        return jsonify({"error": "无效类型"}), 400
        
    if not recipe:
        return jsonify({"error": "菜谱未找到"}), 404
        
    # 转换为与生成菜谱相同的结构
    return jsonify({
        "recipe": recipe.recipe,
        "dish_image": recipe.total_img,
        "steps_images": recipe.steps_imgs,
        "nutrition": recipe.dish_nutrition,
        "uml_sequence": recipe.uml_sequence,
    })

# 收藏菜谱
@app.route('/favorite', methods=['POST'])
def favorite():
    if 'username' not in session:
        return jsonify({'success': False, 'message': '未登录'}), 401
    username = session['username']
    user = User(username)
    data = request.get_json()
    try:
        # 构造 Recipe 对象
        print(f"Loading recipe from history: {data['name']}.json")
        recipe = user.load_recipe_from_history(data['name']+".json")
        if not recipe:
            return jsonify({'success': False, 'message': '菜谱未找到'}), 404
        
        user.save_recipe_to_likes(recipe)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error saving recipe to favorites: {e}")
        return jsonify({'success': False, 'message': str(e)})
    
# 删除菜谱
@app.route('/delete_recipe', methods=['POST'])
def delete_recipe():
    if 'username' not in session:
        return jsonify({'success': False, 'message': '未登录'}), 401
    username = session['username']
    user = User(username)
    data = request.get_json()
    recipe_type = data.get('type')
    filename = data.get('filename')
    try:
        if recipe_type == 'likes':
            user.delete_recipe_from_likes(filename)
        elif recipe_type == 'history':
            user.delete_recipe_from_history(filename)
        else:
            return jsonify({'success': False, 'message': '类型错误'})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# 清除历史记录
@app.route('/clear_history', methods=['POST'])
def clear_history():
    if 'username' not in session:
        return jsonify({'success': False, 'message': '未登录'}), 401
    username = session['username']
    user = User(username)
    try:
        user.clear_history()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)