from utils.generate_recipe import generate_recipe
from utils.generate_image_description import generate_image_description
from utils.generate_dish_image import generate_dish_image
from utils.generate_steps_image import generate_steps_image
from utils.generate_nutritional_analysis import generate_nutrition_analysis
from utils.generate_diagram import build_sequence
from utils.generate_prefer_recipe import generate_prefer_recipe
import base64
from io import BytesIO
from classes.class_recipe import Recipe
import json

class RecipeGenerationPipeline:
    """
    菜谱生成流水线类，用于根据食材、菜系及用户偏好生成完整的菜谱信息。

    该流水线包含以下步骤：
    1. 生成菜谱（根据用户偏好选择不同生成接口）
    2. 生成菜谱名称
    3. 生成菜品外观描述
    4. 生成菜品主图像
    5. 生成营养分析数据
    6. 生成菜谱制作步骤的UML序列图
    7. 生成每个步骤对应的图片

    最终输出包含所有信息的 Recipe 对象。

    Attributes:
        ingredients (str): 用户输入的食材列表字符串。
        cuisine_type (str): 菜系类型，如“川菜”、“意大利菜”等。
        preferences (str|None): 用户口味及偏好描述，默认无。
        recipe (dict|None): 生成的菜谱详细信息。
        name (str|None): 菜谱名称。
        appearance_desc (str|None): 菜品外观描述文本。
        dish_image (PIL.Image|None): 菜品主图像。
        nutrition (dict|None): 菜品营养分析数据。
        uml_sequence (PIL.Image|None): 菜谱步骤的UML序列图。
        step_images (list[PIL.Image]|None): 菜谱每个步骤对应的图片列表。

    Methods:
        execute():
            执行完整的菜谱生成流程，返回包含所有生成信息的 Recipe 对象，或包含错误信息的字典。
        format_response():
            将生成的图片转换为Base64编码，并构建Recipe对象。
        image_to_base64(image):
            静态方法，将PIL.Image对象转换为Base64字符串。
    """
    def __init__(self, ingredients, cuisine_type,preferences=None):
        self.ingredients = ingredients
        self.cuisine_type = cuisine_type
        self.recipe = None
        self.appearance_desc = None
        self.dish_image = None
        self.nutrition = None
        self.step_images = None
        self.name = None
        self.uml_sequence = None
        self.preferences=preferences
    
    def execute(self):
        """执行完整的菜谱生成流程"""
        try:
            if self.preferences==None:
                self.recipe = generate_recipe(
                    ingredients=self.ingredients,
                    cuisine_type=self.cuisine_type
                )
                print("recipe done")
            else :
                self.recipe = generate_prefer_recipe(
                    ingredients=self.ingredients,
                    cuisine_type=self.cuisine_type
                )
                print("recipe done")

            self.name = self.recipe.get("name")
            if not self.name:
                self.name = "未知菜谱"
                print("未能生成菜谱名称，使用默认名称 '未知菜谱'")

            self.appearance_desc = generate_image_description(self.recipe)
            print("appearance_desc done")

            self.dish_image = generate_dish_image(self.appearance_desc)
            print("dish_image done")

            self.nutrition = generate_nutrition_analysis(self.recipe)
            print("nutrition done")

            self.uml_sequence = build_sequence(self.recipe)
            print("uml done")

            self.step_images = generate_steps_image(self.recipe)
            print("step_image done")


            return self.format_response()
        except Exception as e:
            return {"error": str(e)}
    
    def format_response(self):
        """格式化生成结果为API响应格式"""

        dish_base64 = self.image_to_base64(self.dish_image)
        step_base64 = [self.image_to_base64(img) for img in self.step_images]
        uml_base64 = self.image_to_base64(self.uml_sequence)

        return Recipe(
            name=self.name,
            recipe=self.recipe,
            steps_imgs=step_base64,
            total_img=dish_base64, 
            dish_nutrition=self.nutrition,
            uml_sequence=uml_base64
        )
    
    @staticmethod
    def image_to_base64(image):
        """将PIL图像转换为base64字符串"""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')