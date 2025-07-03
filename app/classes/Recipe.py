import json
import os

#食谱类
class Recipe:
    """
    表示一个菜谱的类，包含菜谱名称、步骤、图片、营养信息及相关 UML 顺序图信息。

    属性:
        name (str): 菜谱名称。
        recipe (list): 菜谱详细步骤和材料信息的列表。
        steps_imgs (list): 每个步骤对应的图片路径或图片对象列表。
        total_img (str): 完成菜品的图片路径或图片对象。
        dish_nutrition (dict): 菜谱的营养信息字典，如热量、蛋白质、脂肪等。
        uml_sequence (any): 与菜谱相关的 UML 顺序图数据，用于描述工序或流程。

    方法:
        to_dict(): 将菜谱对象转换为字典格式，方便序列化或保存。
    """
    def __init__(self, name, recipe, steps_imgs, total_img, dish_nutrition, uml_sequence):
        """
        初始化 Recipe 对象

        参数:
        - name (str): 菜谱名称
        - recipe (list): 菜谱详细步骤及材料等
        - steps_imgs (list): 每个步骤对应的图片路径或对象列表
        - total_img (str): 完成菜品的图片路径或对象
        - dish_nutrition (dict): 菜谱的营养信息
        - uml_sequence (any): UML顺序图信息
        """
        self.name = name
        self.recipe = recipe
        self.steps_imgs = steps_imgs 
        self.total_img = total_img
        self.dish_nutrition = dish_nutrition
        self.uml_sequence = uml_sequence


    def to_dict(self):
        """将 Recipe 对象转换为字典"""
        return {
            "name": self.name,
            "recipe": self.recipe,
            "steps_imgs": self.steps_imgs,
            "total_img": self.total_img,
            "dish_nutrition": self.dish_nutrition,
            "uml_sequence": self.uml_sequence
        }


def load_recipe(file_path):
    """
    从 JSON 文件加载食谱数据，并返回 Recipe 实例。

    参数:
    - file_path (str): JSON 文件路径

    返回:
    - Recipe 对象

    异常:
    - FileNotFoundError: 文件不存在时抛出
    - ValueError: 数据不完整时抛出
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    

    with open(file_path, 'r', encoding='utf-8') as f:    
        data = json.load(f)
        name = data.get('name')
        recipe = data.get('recipe', [])
        steps_imgs = data.get('steps_imgs', [])
        total_img = data.get('total_img')
        dish_nutrition = data.get('dish_nutrition', {})
        uml_sequence = data.get('uml_sequence', None)

        if not name or not recipe or not total_img:
            print(f"文件 {file_path} 数据不完整")
            raise ValueError("食谱数据不完整")
        return Recipe(name, recipe, steps_imgs, total_img, dish_nutrition, uml_sequence)
    
#测试
if __name__ == "__main__":
    # 假设有一个名为recipe.json的文件
    recipe = load_recipe('recipe_example.json')
    print(recipe.to_dict())
    # 输出: {'name': '番茄炒蛋', 'recipe': [...], 'steps_imgs': [...], 'total_img': '...', 'dish_nutrition': {...}}