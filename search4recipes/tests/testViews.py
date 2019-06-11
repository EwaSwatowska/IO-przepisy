from unittest import mock
from django.test import TestCase
from search4recipes import views
from search4recipes.models import Ingredient


class testViews(TestCase):
    @mock.patch('django.template.loader.render_to_string')
    @mock.patch('search4recipes.models.Ingredient.objects.all')
    def test_home(self, mock_all, mock_render_to_string):
        mock_all.return_value = {type('', (object,), {"ingredient_name": "pietruszka"})()}
        views.home(request="")
        mock_all.assert_called()
        self.assertIn("'lista': ['pietruszka'],", str(mock_render_to_string.call_args))

    @mock.patch('django.template.loader.render_to_string')
    @mock.patch('search4recipes.models.Recipe.objects.get')
    def test_recipe_detail_contains_ingredients(self, mock_get, mock_render_to_string):
        ingredient = type('', (object,), {"ingredient_name": "pietruszka"})()
        ingredients_in_recipe = type('', (object,), {"all": lambda a: {ingredient}})()
        mock_get.return_value = type('', (object,), {"ingredientsinrecipes_set": ingredients_in_recipe})()
        views.recipe_detail("", 5)
        mock_get.assert_called()
        self.assertIn(str(ingredient), str(mock_render_to_string.call_args))

    @mock.patch('django.template.loader.render_to_string')
    @mock.patch('search4recipes.models.Recipe.objects.get')
    def test_recipe_detail_contains_recipe(self, mock_get, mock_render_to_string):
        ingredient = None
        ingredients_in_recipe = type('', (object,), {"all": lambda a: {ingredient}})()
        mock_get.return_value = type('', (object,), {"ingredientsinrecipes_set": ingredients_in_recipe})()
        views.recipe_detail("", 5)
        mock_get.assert_called()
        self.assertIn(str(mock_get()), str(mock_render_to_string.call_args))

    def test_difficult_level(self):
        def get_request_with_specified_difficult(level_name):
            get_array = {'difficulty-level': level_name}
            return type('', (object,), {"GET": get_array})()

        self.assertEqual(None, views.get_difficulty_level(get_request_with_specified_difficult("Inny")))
        self.assertEqual(None, views.get_difficulty_level(get_request_with_specified_difficult("Dowolny")))
        self.assertEqual(0, views.get_difficulty_level(get_request_with_specified_difficult("Łatwy")))
        self.assertEqual(1, views.get_difficulty_level(get_request_with_specified_difficult("Średni")))
        self.assertEqual(2, views.get_difficulty_level(get_request_with_specified_difficult("Trudny")))

    @mock.patch('django.core.paginator.Paginator.get_page')
    @mock.patch('search4recipes.models.Ingredient.objects.get')
    @mock.patch('django.template.loader.render_to_string')
    @mock.patch('search4recipes.models.Recipe.get_filtered_recipes')
    def test_recipe_list_partition_ingredients(self, mock_get_filtered_recipes, mock_render_to_string, mock_get,
                                               mock_get_page):
        get_list = {"ingredient-list1": "marchew1", "isPositive1": 'on',
                    "ingredient-list2": "marchew2", "isPositive2": 'off',
                    "ingredient-list3": "marchew3", "isPositive3": 'asd',
                    "ingredient-list4": "marchew4", "isPositive4": '1',
                    "ingredient-list5": "marchew5", "isPositive5": '',
                    "ingredient-list0": "", "isPositive0": 'on',
                    "ingredient-1": "marchew87", 'difficulty-level': 'Dowolny',
                    'min-time': 0, 'max-time': 100};
        mock_get_page.return_value = lambda a: a
        request = type('', (object,), {"GET": get_list})()
        recipes = ["Recipe no1"];
        mock_get_filtered_recipes.return_value = type('', (object,), {"recipes": recipes, "count": lambda a: 1})();
        views.recipe_list(request);
        self.assertIn("['marchew1'], ['marchew2']", str(mock_get_filtered_recipes.call_args))

    @mock.patch("search4recipes.views.home")
    @mock.patch('search4recipes.models.Ingredient.objects.get')
    @mock.patch('django.template.loader.render_to_string')
    @mock.patch('search4recipes.models.Recipe.get_filtered_recipes')
    def test_recipe_list_ingredient_doesnt_exist(self, mock_get_filtered_recipes, mock_render_to_string, mock_get,
                                                 mock_home):
        get_list = {"ingredient-list1": "marchew1", "isPositive1": 'on',
                    "ingredient-list2": "marchew2", "isPositive2": 'off',
                    "ingredient-list3": "marchew3", "isPositive3": 'asd',
                    "ingredient-list4": "marchew4", "isPositive4": '1',
                    "ingredient-list5": "marchew5", "isPositive5": '',
                    "ingredient-list0": "", "isPositive0": 'on',
                    "ingredient-1": "marchew87"}

        request = type('', (object,), {"GET": get_list})()
        mock_get.side_effect = Ingredient.DoesNotExist()
        views.recipe_list(request)
        self.assertTrue(mock_home.called)
        self.assertIn("marchew1", str(mock_home.call_args))

    @mock.patch('search4recipes.models.Recipe.objects.get')
    def test_update_mark_good_value(self, mock_get):
        params = {"recipe_id": 1, "mark": 0}
        r = type('', (object,), {"is_ajax": lambda a: True, "GET": params})()
        recipe = type('', (object,), {"save": lambda a: a, "rate": 2, "amount_of_rates": 0})()
        mock_get.return_value = recipe

        with self.assertRaises(ValueError):
            views.update_mark(r)

        params["mark"] = 3
        views.update_mark(r)
        self.assertEquals(recipe.amount_of_rates, 1)
        self.assertEquals(recipe.rate, 3)

        params["mark"] = 5
        views.update_mark(r)
        self.assertEquals(recipe.amount_of_rates, 2)
        self.assertEquals(recipe.rate, 4)

        params["mark"] = 10
        with self.assertRaises(ValueError):
            views.update_mark(r)

    @mock.patch('search4recipes.models.Recipe.objects.get')
    def test_update_mark_divide_by_0(self, mock_get):
        params = {"recipe_id": 1, "mark": 0}
        r = type('', (object,), {"is_ajax": lambda a: True, "GET": params})()
        recipe = type('', (object,), {"save": lambda a: a, "rate": 2, "amount_of_rates": -1})()
        mock_get.return_value = recipe
        with self.assertRaises(ValueError):
            views.update_mark(r)
