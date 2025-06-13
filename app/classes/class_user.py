import os
import json

from gradio_client import file
from classes.class_recipe import load_recipe, Recipe
from classes.RecipeGenerationPipeline import RecipeGenerationPipeline
from collections import Counter
import numpy as np

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
        self.preferences_file = os.path.join(self.filepath, "likes/preferences.json")
        self.update_preferences_file()

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
        
        # 如果没有收藏，返回空偏好
        if not self.likes:
            return preferences
        
        ingredient_counter = Counter()
        nutrition_sums = {"calories": 0, "protein": 0, "fat": 0}
        flavor_sums = {"spicy": 0, "sweet": 0, "sour": 0, "salty": 0, "bitter": 0}
        category_counter = Counter()
        cooking_times = []
        
        # 分析每个收藏菜谱
        for like in self.likes:
            filename = like["filename"]
            recipe = self.load_recipe_from_likes(filename)
            
            if recipe:
                # 食材偏好
                for ingredient in recipe.recipe:
                    ingredient_counter[ingredient] += 1
                
                # 营养偏好（平均值）
                if recipe.dish_nutrition:
                    for nutrient in nutrition_sums:
                        if nutrient in recipe.dish_nutrition:
                            nutrition_sums[nutrient] += recipe.dish_nutrition[nutrient]
                
                # 口味偏好（如果有）
                if hasattr(recipe, 'flavors') and recipe.flavors:
                    for flavor in flavor_sums:
                        if flavor in recipe.flavors:
                            flavor_sums[flavor] += recipe.flavors[flavor]
                
                # 类别偏好（如果有）
                if hasattr(recipe, 'categories') and recipe.categories:
                    for category in recipe.categories:
                        category_counter[category] += 1
                
                # 烹饪时间偏好
                if hasattr(recipe, 'cooking_time') and recipe.cooking_time:
                    cooking_times.append(recipe.cooking_time)
        
        # 计算食材偏好权重（归一化）
        total_ingredients = sum(ingredient_counter.values())
        for ingredient, count in ingredient_counter.items():
            preferences["ingredient_preferences"][ingredient] = round(count / total_ingredients, 3)
        
        # 计算营养平均值
        num_recipes = len(self.likes)
        for nutrient in preferences["nutrition_preferences"]:
            preferences["nutrition_preferences"][nutrient] = round(nutrition_sums[nutrient] / num_recipes, 1)
        
        # 计算口味平均值
        for flavor in preferences["flavor_preferences"]:
            preferences["flavor_preferences"][flavor] = round(flavor_sums[flavor] / num_recipes, 1)
        
        # 计算类别偏好权重
        total_categories = sum(category_counter.values())
        for category, count in category_counter.items():
            preferences["category_preferences"][category] = round(count / total_categories, 3)
        
        # 计算平均烹饪时间（中位数）
        if cooking_times:
            preferences["cooking_time_preference"] = int(np.median(cooking_times))
        
        return preferences
    
    def update_preferences_file(self):
        """
        更新用户偏好文件
        """
        preferences = self.generate_preferences()
        try:
            with open(self.preferences_file, "w", encoding="utf-8") as f:
                json.dump(preferences, f, ensure_ascii=False, indent=4)
            pipline = RecipeGenerationPipeline(None,None,preferences)
            result = pipline.execute()
            self.save_recipe_to_history(result,True)
            print(f"update preferences.")
            return True
        except Exception as e:
            print(f"Error updating preferences file: {str(e)}")
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
    
    def save_recipe_to_likes(self, recipe):
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
        dish_nutrition={"calories": 200, "protein": 10, "fat": 5}
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
