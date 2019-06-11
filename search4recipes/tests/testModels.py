# -*- coding: utf-8 -*-
from unittest import mock
from django.test import TestCase
from search4recipes.models import Ingredient, Measurement, IngredientsInRecipes, Recipe


class testMeasurment(TestCase):
    def setUp(self):
        self.m1 = Measurement()
        self.m1.unit = "mG"
        self.m1.measurement_use = "miliGram"

    def test_measurment_unit_is_unique(self):
        try:
            m2 = Measurement()
            m2.unit = "mG"
            m2.measurement_use = "miliGram"
            self.fail("Measurments units arent unique")
        except:
            pass

    def test_measurment_uses_arent_unique(self):
        try:
            m2 = Measurement()
            m2.unit = "kG"
            m2.measurement_use = "miliGram"
        except:
            self.fail("Measurments uses neednt be unique")


class testRecipe(TestCase):

    def addNewRecipe(self, title, ingredients, time=10, level=1):
        self.recipe = \
            Recipe.objects.update_or_create(recipe_title=title, preparation_time=time, difficulty_level=level)[0]
        self.measurment = Measurement.objects.get_or_create(unit="kG", measurement_use="kilogram")[0]
        for ingredient in ingredients:
            self.ingredient = Ingredient.objects.get_or_create(ingredient_name=ingredient)[0]
            self.ingredients_in_recipes = IngredientsInRecipes.objects.create(ingredient=self.ingredient,
                                                                              measurement=self.measurment,
                                                                              recipe=self.recipe)

    def test_is_recipe_title_unique(self):
        try:
            self.addNewRecipe("Bananowy deser", {"Banan"})
            self.addNewRecipe("Bananowy deser", {"Czerwony Banan"})
            self.fail("Recipe titles aren't unique!")
        except:
            pass

    def test_get_filtered_recipes_with_valid_ingredient(self):
        self.addNewRecipe("Bananowy deser", {"Banan"})
        self.addNewRecipe("Bananowy deser z czerwonych bananow", {"Czerwony Banan"})
        results = Recipe.get_filtered_recipes(("Banan",))
        self.assertNotIn("Bananowy deser z czerwonych bananow",
                         str(results))
        self.assertIn("Bananowy deser", str(results))

    def test_get_filtered_recipes_with_valid_ingredient_should_return_1_result(self):
        self.addNewRecipe("Bananowy deser", {"Banan"})
        self.addNewRecipe("Bananowy deser z czerwonych bananow", {"Czerwony Banan"})
        results = Recipe.get_filtered_recipes(("Czerwony Banan",))
        self.assertIn("Bananowy deser z czerwonych bananow", str(results))
        self.assertEqual(results.count(), 1)

    def test_get_filtered_recipes_all(self):
        self.addNewRecipe("Bananowy deser", {"Banan"})
        self.addNewRecipe("Bananowy deser z czerwonych bananow", {"Czerwony Banan"})
        results = Recipe.get_filtered_recipes()
        self.assertEqual(results.count(), 2)

    def test_get_filtered_recipes_should_find_0_recipes(self):
        self.addNewRecipe("Bananowy deser", {"Banan"})
        self.addNewRecipe("Bananowy deser z czerwonych bananow", {"Czerwony Banan"})
        results = Recipe.get_filtered_recipes(ingredients_not={"Banan", "Czerwony Banan"})
        self.assertEqual(results.count(), 0)

    def test_get_filtered_recipes_preparation_time_min(self):
        self.addNewRecipe("Lody ze sklepu", {"Lody"}, time=0)
        self.addNewRecipe("Bananowy deser", {"Banan"}, time=30)
        self.addNewRecipe("Bananowy deser z czerwonych bananow", {"Czerwony Banan"}, time=-10)
        self.addNewRecipe("Ziemniaki z kurczakiem", {"Kurczak", "Ziemniaki"}, time=30.9)

        fasterOrEqualThan30min = Recipe.get_filtered_recipes(max_time=30)
        fasterOrEqualThan0min = Recipe.get_filtered_recipes(max_time=0)
        slowerOrEqualThan0min = Recipe.get_filtered_recipes(min_time=0)
        slowerOrEqualThan30min6sec = Recipe.get_filtered_recipes(min_time=30.1)
        beetwen30And30min30sec = Recipe.get_filtered_recipes(min_time=30, max_time=30.5)
        beetwen40And30min = Recipe.get_filtered_recipes(min_time=40, max_time=30)
        negativePreparationTime = Recipe.get_filtered_recipes(max_time=-1)

        self.assertEqual(fasterOrEqualThan30min.count(), 4)
        self.assertEqual(fasterOrEqualThan0min.count(), 2)
        self.assertEqual(slowerOrEqualThan0min.count(), 3)
        self.assertEqual(slowerOrEqualThan30min6sec.count(), 0)
        self.assertEqual(beetwen30And30min30sec.count(), 2)
        self.assertEqual(beetwen40And30min.count(), 0)
        self.assertEqual(negativePreparationTime.count(), 1)

    def test_get_filtered_recipes_difficult(self):
        self.addNewRecipe("Deser lvl 1", {"Lody"}, level=1)
        self.addNewRecipe("Deser lvl 1.2", {"Banan"}, level=1.2)
        self.addNewRecipe("Deser lvl 2", {"Czerwony Banan"}, level=2)
        self.addNewRecipe("Deser lvl 3", {"Czerwony Banan"}, level=3)
        self.addNewRecipe("Deser lvl 4", {"Czerwony Banan"}, level=4)
        self.addNewRecipe("Deser lvl -1", {"Czerwony Banan"}, level=-1)
        self.addNewRecipe("Deser lvl 0", {"Czerwony Banan"}, level=0)

        self.assertEqual(1, Recipe.get_filtered_recipes(
            difficulty_level=0).count())  # Byc moze nie powinno akceptowac lvl innych niz [1,2,3]
        self.assertEqual(2, Recipe.get_filtered_recipes(difficulty_level=1).count())
        self.assertEqual(1, Recipe.get_filtered_recipes(difficulty_level=2).count())
        self.assertEqual(1, Recipe.get_filtered_recipes(difficulty_level=3).count())
        self.assertEqual(1, Recipe.get_filtered_recipes(difficulty_level=4).count())
        self.assertEqual(1, Recipe.get_filtered_recipes(difficulty_level=-1).count())
        self.assertEqual(2, Recipe.get_filtered_recipes(difficulty_level=1.2).count())
