
from classes.RecipeGenerationPipeline import RecipeGenerationPipeline
if __name__ == "__main__":
    ingredients = "辣椒、猪肉、白菜、虾仁、鸡蛋、玉米粒"
    cuisine_type = "中式粤菜"

    pipline = RecipeGenerationPipeline(ingredients, cuisine_type)
    result = pipline.execute()


