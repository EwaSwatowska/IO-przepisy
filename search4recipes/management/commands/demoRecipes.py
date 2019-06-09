from django.core.management import BaseCommand
from search4recipes.models import Ingredient, Measurement, IngredientsInRecipes, Recipe


class Command(BaseCommand):
    help = 'Dodaje przykładowe przepisy do bazy danych.'

    def handle(self, *args, **options):
        IngredientsInRecipes.objects.all().delete()
        Ingredient.objects.all().delete()
        Measurement.objects.all().delete()
        Recipe.objects.all().delete()
        ingredients = ['Marchewka', 'Groszek', 'Kurczak', 'Pieprz', 'Sól']
        for ingredient_item in ingredients:
            ingredient = Ingredient()
            ingredient.ingredient_name = ingredient_item
            ingredient.save()
        measurements = [('Kilogram', 'kg'), ('Gram', 'g'), ('Sztuka', 'x sztuka'), ('Szczypta', 'x szczypta')]
        for measurement_item in measurements:
            measurement = Measurement()
            measurement.unit = measurement_item[0]
            measurement.measurement_use = measurement_item[1]
            measurement.save()
        recipes = [('Marchewka z marchewką', '1.Pokrój marchewkę. 2.Zjedz', [('Marchewka', 1, "Kilogram")]),
                   ('Marchewka z groszkiem', '1.Pokrój Marchewkę.<br> 2.Dodaj Groszek.<br> 3. Zjedz',
                    [('Marchewka', 1, "Kilogram"), ('Groszek', 1, "Gram")])]
        for recipe_list in recipes:
            recipe = Recipe()
            recipe.recipe_title = recipe_list[0]
            recipe.text = recipe_list[1]
            recipe.save()
            for ingredient_list in recipe_list[2]:
                ingredient = IngredientsInRecipes()
                ingredient.recipe = recipe
                ingredient.ingredient = Ingredient.objects.get(ingredient_name=ingredient_list[0])
                ingredient.measurement = Measurement.objects.get(unit=ingredient_list[2])
                ingredient.amount = ingredient_list[1]
                ingredient.save()
