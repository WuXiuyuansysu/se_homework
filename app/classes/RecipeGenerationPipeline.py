from utils.generate_recipe import generate_recipe
from utils.generate_image_description import generate_image_description
from utils.generate_dish_image import generate_dish_image
from utils.generate_steps_image import generate_steps_image
from utils.generate_nutritional_analysis import generate_nutrition_analysis
import base64
from io import BytesIO

class RecipeGenerationPipeline:
    def __init__(self, ingredients, cuisine_type):
        self.ingredients = ingredients
        self.cuisine_type = cuisine_type
        self.recipe = None
        self.appearance_desc = None
        self.dish_image = None
        self.nutrition = None
        self.step_images = None
    
    def execute(self):
        """执行完整的菜谱生成流程"""
        try:
            self.recipe = generate_recipe(
                ingredients=self.ingredients,
                cuisine_type=self.cuisine_type
            )
            print("recipe done")

            self.appearance_desc = generate_image_description(self.recipe)
            print("appearance_desc done")

            self.dish_image = generate_dish_image(self.appearance_desc)
            print("dish_image done")

            self.nutrition = generate_nutrition_analysis(self.recipe)
            print("nutrition done")

            self.step_images = generate_steps_image(self.recipe)
            print("step_image done")

            return self.format_response()
        except Exception as e:
            return {"error": str(e)}
    
    def format_response(self):
        """格式化生成结果为API响应格式"""

        dish_base64 = self.image_to_base64(self.dish_image)
        step_base64 = [self.image_to_base64(img) for img in self.step_images]
        
        return {
            "recipe": self.recipe,
            "steps_images": step_base64,
            "dish_image": dish_base64, 
            "nutrition": self.nutrition 
        }
    
    @staticmethod
    def image_to_base64(image):
        """将PIL图像转换为base64字符串"""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')