from django.core.management import BaseCommand
from search4recipes.models import Ingredient, Measurement, IngredientsInRecipes, Recipe


class Command(BaseCommand):
    help = 'Dodaje przykładowe przepisy do bazy danych.'

    def handle(self, *args, **options):
        IngredientsInRecipes.objects.all().delete()
        Ingredient.objects.all().delete()
        Measurement.objects.all().delete()
        Recipe.objects.all().delete()
        ingredients = ['Marchewka', 'Groszek', 'Kurczak', 'Pieprz', 'Sól', 'Ryż', 'Kiełbasa', 'Cebula', 'Pomidor',
                       'Oliwa', 'Kurkuma', 'Bulion']
        for ingredient_item in ingredients:
            ingredient = Ingredient()
            ingredient.ingredient_name = ingredient_item
            ingredient.save()
        measurements = [('Kilogram', 'kg'), ('Gram', 'g'), ('Sztuka', 'x sztuka'), ('Szczypta', 'x szczypta'),
                        ('Litr', 'l'), ('Łyżka', 'x łyżka'), ('Łyżeczka', 'x łyżeczka')]
        for measurement_item in measurements:
            measurement = Measurement()
            measurement.unit = measurement_item[0]
            measurement.measurement_use = measurement_item[1]
            measurement.save()
        recipes = [('Marchewka z marchewką', '1. Pokrój marchewkę.<br>2. Zjedz', 0, 3, [('Marchewka', 1, 'Kilogram')]),
                   ('Marchewka z groszkiem', '1. Pokrój Marchewkę.<br>2. Dodaj Groszek.<br>3.Zjedz', 0, 5,
                    [('Marchewka', 0.5, 'Kilogram'), ('Groszek', 100, 'Gram')]),
                   ('Kurczak w marchewce', '1. Umyj kurczaka.<br>2. Przypraw go solą i pieprzem.<br>3. Umieść w formie'
                                           ' kurczaka i wypełnij marchewką startą na tarce o grubych oczkach.<br>4. '
                                           'Całość umieść w piekraniku na 90min. w temperaturze 200 stopni Celcjusza',
                    1, 120, [('Marchewka', 0.25, 'Kilogram'), ('Kurczak', 0.25, 'Sztuka'), ('Sól', 1, 'Szczypta'),
                             ('Pieprz', 1, 'Szczypta')]),
                   ('Marchewka w mundurkach', '1. Ugotuj marchewkę bez obierania.<br>2. Zjedz', 0, 15,
                    [('Marchewka', 1, 'Kilogram')]),
                   ('Kiełbasa po studencku', '1. Pokrój cebulę w piórka.<br>2. Usmaż razem z kiełbasą', 0, 20,
                    [('Kiełbasa', 2, 'Sztuka'), ('Cebula', 1, 'Sztuka')]),
                   ('Ryż z kiełbasą i groszkiem', '1. Oliwę rozgrzej na głębokiej patelni.<br>2. Dodaj posiekaną cebulę'
                                                  ' i pokrojoną w plasterki kiełbasę, smaż na średnim ogniu 3-4 minuty.'
                                                  '<br>3.Dodaj ryż i smaż minutę.<br>4.W tym czasie dodaj kurkumę i pok'
                                                  'rojone w kostkę pomidory, następnie zwiększ ogień i polej całość poł'
                                                  'ową bulionu tak, aby przykryła ryż.<br>5.Posyp delikatnie solą.<br>6'
                                                  '.Po zagotowaniu zmniejsz ogień i od czasu do czasu mieszając, podlew'
                                                  'aj ryż bulionem przez 15 minut, aż wchłonie większość bulionu i będz'
                                                  'ie prawie miękki.<br>6.Następnie dodaj groszek - podlej resztką buli'
                                                  'onu.<br>7.Przykryj całość i gotuj na małym ogniu, aż ryż wchłonie bu'
                                                  'lion.', 2, 60,
                    [('Ryż', 150, 'Gram'), ('Kiełbasa', 100, 'Gram'), ('Groszek', 100, 'Gram'),
                     ('Bulion', 0.5, 'Litr'), ('Cebula', 1, 'Sztuka'), ('Pomidor', 1.5, 'Sztuka'),
                     ('Oliwa', 0.5, 'Łyżka'), ('Sól', 1, 'Szczypta'), ('Kurkuma', 1, 'Łyżeczka')])
                   ]
        for recipe_list in recipes:
            recipe = Recipe()
            recipe.recipe_title = recipe_list[0]
            recipe.text = recipe_list[1]
            recipe.difficulty_level = recipe_list[2]
            recipe.preparation_time = recipe_list[3]
            recipe.save()
            for ingredient_list in recipe_list[4]:
                ingredient = IngredientsInRecipes()
                ingredient.recipe = recipe
                ingredient.ingredient = Ingredient.objects.get(ingredient_name=ingredient_list[0])
                ingredient.measurement = Measurement.objects.get(unit=ingredient_list[2])
                ingredient.amount = ingredient_list[1]
                ingredient.save()
