import sys
import os
import openai
from openai import OpenAI
# 获取当前文件所在目录的父目录（项目根目录）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)  # 添加到模块搜索路径
import json

from gradio_client import file
from classes.class_recipe import load_recipe, Recipe
from classes.RecipeGenerationPipeline import RecipeGenerationPipeline
from collections import Counter
import numpy as np
import config
class User:
    """
    用户类，用于管理单个用户的菜谱收藏、历史记录及偏好数据。

    Attributes:
        username (str): 用户名，用于定位用户文件夹。
        filepath (str): 用户数据根目录路径。
        likes (list): 用户收藏的菜谱列表，包含文件名和数据。
        history (list): 用户历史记录列表，包含文件名和数据。
        preferences_file (str): 用户偏好数据的文件路径。

    方法:
        load_user_likes(): 加载用户收藏的菜谱列表。
        load_user_history(): 加载用户历史记录列表。
        generate_preferences(): 根据收藏菜谱分析生成用户偏好数据。
        update_preferences_file(): 更新用户偏好文件，并触发偏好相关操作。
        get_preferences(): 获取用户偏好数据，优先读取已存在的偏好文件。
        save_recipe_to_likes(recipe): 保存菜谱到收藏夹，更新收藏和偏好。
        load_recipe_from_likes(filename): 从收藏夹加载指定菜谱。
        load_recipe_from_history(filename): 从历史记录加载指定菜谱。
        save_recipe_to_history(recipe, prefer=False): 保存菜谱到历史记录，prefer=True时保存为偏好文件。
        create_user_folder(): 创建用户根文件夹。
        create_likes_folder(): 创建用户收藏文件夹。
        create_history_folder(): 创建用户历史记录文件夹。
        setup(): 创建用户相关的所有文件夹。
    """
    def __init__(self, username: str):
        self.username = username
        self.filepath = "./data/user_data/"+self.username
        self.likes = self.load_user_likes()
        self.history = self.load_user_history()
        self.preferences_file = os.path.join(self.filepath, "preferences.json")
        self.advice_file=os.path.join(self.filepath, "advice.json")

    def load_user_history(self):
        """
        遍历历史记录文件夹，返回包含文件名和数据的列表
        """
        path = self.filepath + "/history"
        history_list = []
        if not os.path.exists(path):
            return history_list
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                file_path = os.path.join(path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # 返回文件名和数据的字典
                        history_list.append({
                            "filename": filename,
                            "data": data
                        })
                except Exception:
                    print(f"Error loading file {filename}: {str(Exception)}")
                    continue
        return history_list
   
    def generate_preferences(self):
        """
        分析用户收藏菜谱，生成偏好数据
        返回格式: {
            "ingredient_preferences": {"食材1": 权重, "食材2": 权重, ...},
            "nutrition_preferences": {"calories": 值, "protein": 值, "fat": 值},
            "flavor_preferences": {"spicy": 程度, "sweet": 程度, ...},
            "category_preferences": {"category1": 权重, ...},
            "cooking_time_preference": 平均时间
        }
        """
        preferences = {
            "ingredient_preferences": {},
            "nutrition_preferences": {"calories": 0, "protein": 0, "fat": 0},
            "flavor_preferences": {"spicy": 0, "sweet": 0, "sour": 0, "salty": 0, "bitter": 0},
            "category_preferences": {},
            "cooking_time_preference": 0
        }
        
        if not self.likes:
            return preferences
        
        ingredient_counter = Counter()
        nutrition_sums = {"calories": 0, "protein": 0, "fat": 0}
        flavor_sums = {"spicy": 0, "sweet": 0, "sour": 0, "salty": 0, "bitter": 0}
        category_counter = Counter()
        cooking_times = []
        # 收集所有食材用于AI分析
        all_ingredients = []
        for like in self.likes:
            filename = like["filename"]
            recipe = self.load_recipe_from_likes(filename)
            
            if recipe:
                # 收集食材
                all_ingredients.extend(recipe.recipe)
                # 营养偏好
                if recipe.dish_nutrition:
                    for nutrient in nutrition_sums:
                        if nutrient in recipe.dish_nutrition:
                            nutrition_sums[nutrient] += recipe.dish_nutrition[nutrient]
                
                # 口味偏好
                if hasattr(recipe, 'flavors') and recipe.flavors:
                    for flavor in flavor_sums:
                        if flavor in recipe.flavors:
                            flavor_sums[flavor] += recipe.flavors[flavor]
                
                # 类别偏好
                if hasattr(recipe, 'categories') and recipe.categories:
                    for category in recipe.categories:
                        category_counter[category] += 1
                
                # 烹饪时间偏好
                if hasattr(recipe, 'cooking_time') and recipe.cooking_time:
                    cooking_times.append(recipe.cooking_time)
        # 使用AI标准化食材并计算权重
        print(all_ingredients)
        if all_ingredients:
            prompt = f"""
            你是一个专业厨师助手，需要根据以下食材列表生成标准化的食材偏好分析。
            请严格按照以下规则输出：
            
            ----- 规则 -----
            1. 输出必须是纯净的 JSON 对象
            2. JSON 结构: {{"ingredient_preferences": {{"食材1": 权重, "食材2": 权重, ...}}}}
            3. 处理要求:
            - 将同一种食材的不同名称统一为标准名称(如"番茄"和"西红柿"统一为"番茄")
            - 合并同类食材(如"鸡胸肉"和"鸡肉"统一为"鸡肉")
            - 去除调味品和辅料(盐、糖、酱油等)
            - 计算每种标准化食材的出现频率作为权重(值范围0-1，保留3位小数)
            - 只保留权重≥0.05的食材
            
            ----- 输入数据 -----
            原始食材列表: {all_ingredients}
            """
            
            client = OpenAI(
                api_key=config.API_KEY_1,
                base_url="https://api.suanli.cn/v1"
            )
            
            response = client.chat.completions.create(
                model="free:Qwen3-30B-A3B",
                messages=[
                    {"role": "system", "content": "你是一个专业厨师助手，输出必须是纯净的JSON对象"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            # 解析AI返回的食材偏好
            ai_result = json.loads(response.choices[0].message.content)
            preferences["ingredient_preferences"] = ai_result.get("ingredient_preferences", {})
        
        # 其他偏好保持手动计算
        num_recipes = len(self.likes)
        
        # 营养平均值
        for nutrient in preferences["nutrition_preferences"]:
            preferences["nutrition_preferences"][nutrient] = round(nutrition_sums[nutrient] / num_recipes, 1)
        
        # 口味平均值
        for flavor in preferences["flavor_preferences"]:
            preferences["flavor_preferences"][flavor] = round(flavor_sums[flavor] / num_recipes, 1)
        
        # 类别偏好权重
        total_categories = sum(category_counter.values())
        if total_categories > 0:
            for category, count in category_counter.items():
                preferences["category_preferences"][category] = round(count / total_categories, 3)
        
        # 烹饪时间中位数
        if cooking_times:
            preferences["cooking_time_preference"] = int(np.median(cooking_times))
        
        return preferences
    def generate_nutrition_advice(self,preferences):
        """
        使用AI分析用户收藏菜谱，生成个性化营养建议
        返回格式: {
            "nutrition_analysis": "整体营养分析文本",
            "detailed_advice": {
                "calories": "卡路里建议",
                "protein": "蛋白质建议",
                "fat": "脂肪建议"
            },
            "ingredient_recommendations": ["建议1", "建议2", ...],
            "health_tips": ["健康小贴士1", ...]
        }
        """
        # 获取用户偏好数据
        preferences = self.generate_preferences()
        
        # 准备AI分析提示
        prompt = f"""
        你是一个专业营养师，请根据用户的饮食偏好数据生成个性化营养建议。
        严格按照以下规则输出JSON格式结果：
        
        ----- 输出规则 -----
        1. 必须是纯净JSON对象，包含以下字段:
            - "nutrition_analysis": (字符串) 50-100字的整体营养评估
            - "detailed_advice": (对象) 包含calories/protein/fat三个键的建议文本
            - "ingredient_recommendations": (字符串数组) 3-5条食材调整建议
            - "health_tips": (字符串数组) 2-4条健康生活建议
        
        2. 分析要求:
            - 基于营养数据: {preferences['nutrition_preferences']}
            - 结合口味偏好: {preferences['flavor_preferences']}
            - 参考食材偏好: {preferences['ingredient_preferences']}
            - 考虑烹饪时间: {preferences['cooking_time_preference']}分钟
        
        3. 建议原则:
            - 针对营养不平衡点提出具体改进方案
            - 根据口味偏好推荐替代食材
            - 推荐易获取的本地食材
            - 结合烹饪时间推荐快手健康方案
        
        ----- 用户数据详情 -----
        营养偏好(每道菜平均值):
            - 热量: {preferences['nutrition_preferences']['calories']} kcal
            - 蛋白质: {preferences['nutrition_preferences']['protein']} g
            - 脂肪: {preferences['nutrition_preferences']['fat']} g
        
        口味偏好(1-5分):
            - 辣: {preferences['flavor_preferences']['spicy']}
            - 甜: {preferences['flavor_preferences']['sweet']}
            - 咸: {preferences['flavor_preferences']['salty']}
        
        常用食材(权重): {list(preferences['ingredient_preferences'].items())[:5]}...
        """
        
        client = OpenAI(
            api_key=config.API_KEY_1,
            base_url="https://api.suanli.cn/v1"
        )
        
        response = client.chat.completions.create(
            model="free:Qwen3-30B-A3B",
            messages=[
                {"role": "system", "content": "你是一个专业营养师，输出必须是纯净JSON对象"},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3  # 降低随机性，确保专业建议
        )
        
        # 解析AI返回的营养建议
        try:
            advice = json.loads(response.choices[0].message.content)
            
            # 添加基础数据参考
            advice["reference_data"] = {
                "avg_calories": preferences['nutrition_preferences']['calories'],
                "avg_protein": preferences['nutrition_preferences']['protein'],
                "avg_fat": preferences['nutrition_preferences']['fat']
            }
            
            return advice
        
        except json.JSONDecodeError:
            # 备用方案：返回结构化错误信息
            return {
                "error": "AI分析失败，请稍后再试",
                "fallback_advice": "建议保持饮食多样性，增加蔬菜水果摄入"
            }
    def update_preferences_file(self):
        """
        更新用户偏好文件，同时将营养建议保存到单独文件
        """
        preferences = self.generate_preferences()
        print(f"Generated preferences")
        
        advice = self.generate_nutrition_advice(preferences)
        print(f"Generated nutrition advice")
        
        try:
            # 保存偏好文件
            with open(self.preferences_file, "w", encoding="utf-8") as f:
                json.dump(preferences, f, ensure_ascii=False, indent=4)
            
            # 保存营养建议到新文件（在原文件名后添加 _advice 后缀）
            advice_file = self.advice_file
            with open(advice_file, "w", encoding="utf-8") as f_advice:
                json.dump(advice, f_advice, ensure_ascii=False, indent=4)
            
            pipline = RecipeGenerationPipeline(None, None, preferences)
            result = pipline.execute()
            self.save_recipe_to_history(result, True)
            print(f"Updated preferences and saved nutrition advice separately.")
            return True
        except Exception as e:
            print(f"Error updating files: {str(e)}")
            return False
    
    def get_preferences(self):
        """
        获取用户偏好数据
        """
        # 如果偏好文件存在，直接读取
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        
        # 否则生成新的偏好文件
        return self.generate_preferences()
    
    def save_recipe_to_likes(self, recipe, address=""):
        """
        将Recipe对象保存到收藏夹（likes）文件夹，文件名为菜谱名+".json"
        保存成功后更新收藏列表和偏好文件
        """
        filename = f"{recipe.name}.json"
        path = os.path.join(self.filepath, "likes")
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = os.path.join(path, filename)
        try:
            # 保存菜谱到收藏文件夹
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(recipe.to_dict(), f, ensure_ascii=False, indent=4)
            
            print(f"Recipe '{recipe.name}' saved to likes.")
            self.likes = self.load_user_likes()
            self.update_preferences_file()
            return True
        except Exception as e:
            print(f"Error saving recipe to likes: {str(e)}")
            return False
    
    def load_user_likes(self): 
        """
        遍历收藏文件夹，返回包含文件名和数据的列表
        """
        path = self.filepath + "/likes"
        likes_list = []
        if not os.path.exists(path):
            return likes_list
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                file_path = os.path.join(path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # 返回文件名和数据的字典
                        likes_list.append({
                            "filename": filename,
                            "data": data
                        })
                except Exception:
                    continue
        return likes_list
    
    def load_recipe_from_likes(self, filename):
        """
        根据文件名从收藏夹加载一个菜谱，返回Recipe类对象
        """
        path = os.path.join(self.filepath, "likes", filename)
        if not os.path.exists(path):
            return None
        try:
            return load_recipe(path)
        except Exception:
            return None

    def load_recipe_from_history(self, filename):
        """
        根据文件名从历史记录加载一个菜谱，返回Recipe类对象
        """
        path = os.path.join(self.filepath, "history", filename)
        if not os.path.exists(path):
            return None
        try:
            return load_recipe(path)
        except Exception:
            return None
        

    def save_recipe_to_history(self, recipe,prefer=False):
        """
        将Recipe对象保存到历史记录（history）文件夹，文件名为filename
        """
        if prefer:
            filename = "prefer.json"
            file_path = os.path.join(self.filepath, filename)
        else:
            filename = recipe.name+ ".json"
            path = os.path.join(self.filepath, "history")
            if not os.path.exists(path):
                os.makedirs(path)
            file_path = os.path.join(path, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(recipe.to_dict(), f, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False
        
    def create_user_folder(self):
        """
        创建用户文件夹
        """
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)
        return True
    
    def create_likes_folder(self):
        """
        创建用户收藏文件夹
        """
        likes_path = os.path.join(self.filepath, "likes")
        if not os.path.exists(likes_path):
            os.makedirs(likes_path)
        return True
    
    def create_history_folder(self):
        """
        创建用户历史记录文件夹
        """
        history_path = os.path.join(self.filepath, "history")
        if not os.path.exists(history_path):
            os.makedirs(history_path)
        return True
    
    def setup(self):
        """
        设置用户文件夹和子文件夹
        """
        self.create_user_folder()
        self.create_likes_folder()
        self.create_history_folder()
        return True
    

#测试
if __name__ == "__main__":
    
    user = User( "testuser")
    user.setup()
    print("User folder created:", user.filepath)
    print("Likes folder created:", os.path.join(user.filepath, "likes"))
    print("History folder created:", os.path.join(user.filepath, "history"))
    print("User likes:", user.likes)
    print("User history:", user.history)
    # 测试保存和加载菜谱
    recipe = Recipe(
        name="番茄炒蛋",
        recipe=["番茄", "鸡蛋", "盐", "油"],
        steps_imgs=["step1.png", "step2.png"],
        total_img="total_dish.png",
        dish_nutrition={"calories": 200, "protein": 10, "fat": 5},
        uml_sequence=None
    )
    user.save_recipe_to_likes(recipe, "test_recipe.json")
    user.save_recipe_to_history(recipe, "test_recipe_history.json")
    print("Recipe saved to likes and history.")
    loaded_recipe_likes = user.load_recipe_from_likes("test_recipe.json")
    loaded_recipe_history = user.load_recipe_from_history("test_recipe_history.json")
    print("Loaded recipe from likes:", loaded_recipe_likes)
    print("Loaded recipe from history:", loaded_recipe_history)
    # 测试加载用户喜欢和历史记录
    print("User likes:", user.load_user_likes())
    print("User history:", user.load_user_history())
    # 测试加载菜谱
    recipe = load_recipe('recipe_example.json')
    print(recipe.to_dict())
    # 输出: {'name': '番茄炒蛋', 'recipe': [...], 'steps_imgs': [...], 'total_img': '...', 'dish_nutrition': {...}}
    user.setup()
    print("User setup completed.")
