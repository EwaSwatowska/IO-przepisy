from django.test import TestCase, Client
from search4recipes.models import Recipe, Ingredient, IngredientsInRecipes, Measurement
import json


class testRouter(TestCase):

    def saveInDbNewRecipe(self, title, ingredients, time=10, level=0):
        self.recipe = \
            Recipe.objects.update_or_create(recipe_title=title, preparation_time=time, difficulty_level=level)[0]
        self.measurment = Measurement.objects.get_or_create(unit="kG", measurement_use="kilogram")[0]
        self.measurment.save()
        for ingredient in ingredients:
            self.ingredient = Ingredient.objects.get_or_create(ingredient_name=ingredient)[0]
            self.ingredient.save()
            self.ingredients_in_recipes = IngredientsInRecipes.objects.create(ingredient=self.ingredient,
                                                                              measurement=self.measurment,
                                                                              recipe=self.recipe)
            self.ingredients_in_recipes.save()
        self.recipe.save()
        return self.recipe.id

    def test_home(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_update_mark(self):
        c = Client()
        recipe_id = self.saveInDbNewRecipe("Bananowy deser", {"Banan"})
        response = c.get('/ajax/update_mark', {"mark": 3, "recipe_id": recipe_id},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = json.loads(response.content)
        self.assertEqual(response["ok"], True)
        self.assertEqual(response["rate"], 3)
        self.assertEqual(response["amount_of_rates"], 1)

    def test_recipe_list(self):
        c = Client()
        self.saveInDbNewRecipe("Bananowy deser", {"Banan"})
        list = {"ingredient-list1": "Banan", "isPositive1": 'on',
                "ingredient-list2": "", "isPositive2": '',
                "ingredient-list3": "", "isPositive3": '',
                "ingredient-list4": "", "isPositive4": '',
                "ingredient-list5": "", "isPositive5": '',
                "ingredient-list0": "", "isPositive0": '',
                "min-time": 0, "max-time": 1000,
                "page": 1, 'difficulty-level': 'Łatwy'}
        response = c.get('/recipe_list/', list)
        self.assertInHTML("Bananowy deser", str(response.content))

    def test_recipe_detail(self):
        c = Client()
        id = self.saveInDbNewRecipe("Bananowy deser", {"Banan"})
        response = c.get('/recipe/{}/'.format(id))
        self.assertInHTML("Bananowy deser", str(response.content))
