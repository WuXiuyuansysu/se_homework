from utils.generate_recipe import generate_recipe
from utils.generate_image_description import generate_image_description
from utils.generate_dish_image import generate_dish_image
from utils.generate_steps_image import generate_steps_image

if __name__ == "__main__":
    ingredients = "鸭腿，洋葱，米饭，牛排，西兰花"
    cuisine_type = "中式粤菜"
    recipe = generate_recipe(
        ingredients=ingredients,
        cuisine_type=cuisine_type
    )
    steps_img = generate_steps_image(recipe)
    dish_desciption = generate_image_description(recipe)
    dish_img = generate_dish_image(dish_desciption)