from database import db
from models.subscription import Subscription


vegetarian_meal_1 = Subscription(name='Vegetarian_2_meals', amount_of_meals = 2, price=88.00)
vegetarian_meal_1.save()

vege_meal_2 = Subscription(name='Vegetarian_3_meals', amount_of_meals = 3, price = 131.88)
vege_meal_2.save()

vege_meal_3 = Subscription(name='Vegetarian_4_meals', amount_of_meals = 4, price = 175.84)
vege_meal_3.save()

meat_meal_1 = Subscription(name='Mix_2_meals', amount_of_meals = 2, price = 88.00)
meat_meal_1.save()

meat_meal_2 = Subscription(name='Mix_3_meals', amount_of_meals = 3, price = 131.88)
meat_meal_2.save()

meat_meal_3 = Subscription(name='Mix_4_meals', amount_of_meals = 4, price = 175.84)
meat_meal_3.save()
