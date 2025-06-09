import json
import os

#食谱类
class Recipe:
    def __init__(self, name, recipe, steps_imgs, total_img, dish_nutrition, uml_sequence):
        self.name = name
        self.recipe = recipe
        self.steps_imgs = steps_imgs 
        self.total_img = total_img
        self.dish_nutrition = dish_nutrition
        self.uml_sequence = uml_sequence

    #转化为字典格式
    def to_dict(self):
        return {
            "name": self.name,
            "recipe": self.recipe,
            "steps_imgs": self.steps_imgs,
            "total_img": self.total_img,
            "dish_nutrition": self.dish_nutrition,
            "uml_sequence": self.uml_sequence
        }


def load_recipe(file_path):
    """从JSON文件加载食谱"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    

    with open(file_path, 'r', encoding='utf-8') as f:    
        data = json.load(f)
        name = data.get('name')
        recipe = data.get('recipe', [])
        steps_imgs = data.get('steps_imgs', [])
        total_img = data.get('total_img')
        dish_nutrition = data.get('dish_nutrition', {})
        if not name or not recipe or not total_img:
            print(f"文件 {file_path} 数据不完整")
            raise ValueError("食谱数据不完整")
        return Recipe(name, recipe, steps_imgs, total_img, dish_nutrition)
    
#测试
if __name__ == "__main__":
    # 假设有一个名为recipe.json的文件
    recipe = load_recipe('recipe_example.json')
    print(recipe.to_dict())
    # 输出: {'name': '番茄炒蛋', 'recipe': [...], 'steps_imgs': [...], 'total_img': '...', 'dish_nutrition': {...}}