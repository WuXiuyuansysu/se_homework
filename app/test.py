
from classes.RecipeGenerationPipeline import RecipeGenerationPipeline
if __name__ == "__main__":
    ingredients = "面条，大便，牛肉，猪肉，木耳"
    cuisine_type = "中式粤菜"

    pipline = RecipeGenerationPipeline(ingredients, cuisine_type)
    result = pipline.execute()


