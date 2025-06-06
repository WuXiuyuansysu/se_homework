from utils.generate_recipe import generate_recipe
from utils.generate_image_description import generate_image_description
from utils.generate_dish_image import generate_dish_image
from utils.generate_steps_image import generate_steps_image
from utils.generate_nutritional_analysis import generate_nutrition_analysis
if __name__ == "__main__":
    ingredients = "面条，大便，牛肉，猪肉，木耳"
    cuisine_type = "中式粤菜"
    
    recipe = generate_recipe(
        ingredients=ingredients,
        cuisine_type=cuisine_type
    )
    print(recipe)
    # steps_img = generate_steps_image(recipe)
    
    print("2")
    # dish_desciption = generate_image_description(recipe)
    
    print("3")
    # dish_img = generate_dish_image(dish_desciption)
    print("4")
    dish_nutrition=generate_nutrition_analysis(recipe)
    
    # print(dish_desciption)
    print(dish_nutrition)
