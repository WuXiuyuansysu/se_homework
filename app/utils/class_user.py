import os
import json
from utils.class_recipe import load_recipe, Recipe

class User:
    def __init__(self, username: str):
        self.username = username
        self.filepath = "./data/user_data/"+self.username
        self.likes = self.load_user_likes()
        self.history = self.load_user_history()


    def load_user_history(self):
        """
        遍历历史记录文件夹，返回json列表
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
                        history_list.append(data)
                except Exception:
                    continue
        return history_list
    

    def load_user_likes(self): 
        """
        遍历收藏文件夹，返回json列表
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
                        likes_list.append(data)
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
        
    def save_recipe_to_likes(self, recipe, filename):
        """
        将Recipe对象保存到收藏夹（likes）文件夹，文件名为filename
        """
        path = os.path.join(self.filepath, "likes")
        if not os.path.exists(path):
            os.makedirs(path)
        file_path = os.path.join(path, filename)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(recipe.to_dict(), f, ensure_ascii=False, indent=4)
            return True
        except Exception:
            return False

    def save_recipe_to_history(self, recipe, filename):
        """
        将Recipe对象保存到历史记录（history）文件夹，文件名为filename
        """
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
