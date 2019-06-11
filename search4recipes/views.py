from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from search4recipes import errors
from .models import Recipe, Ingredient


def home(request, error_number: int = None, missing_ingredient: str = None):
    ingredients = [x.ingredient_name for x in Ingredient.objects.all()]
    difficulty_levels = ('Dowolny',) + tuple(x[1] for x in Recipe.DIFFICULTY_CHOICES)
    error: str = None
    if error_number is not None:
        error = errors.ERRORS[error_number]
        if error_number == 1:
            error = error.format(missing_ingredient)
    return render(request, 'glowna.html',
                  {'lista': ingredients, 'levels': difficulty_levels, 'error': error})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = [x for x in recipe.ingredientsinrecipes_set.all()]
    return render(request, 'przepis.html', {'przepis': recipe, 'skladniki': ingredients})


def get_difficulty_level(request):
    difficulty_level = None
    if request.GET['difficulty-level'] != 'Dowolny':
        for x in Recipe.DIFFICULTY_CHOICES:
            if x[1] == request.GET['difficulty-level']:
                difficulty_level = x[0]
    return difficulty_level


def recipe_list(request):
    try:
        ingredients = [request.GET['ingredient-list' + str(i)] for i in range(6) if
                       request.GET['isPositive' + str(i)] == 'on' and request.GET['ingredient-list' + str(i)] != '']
        ingredients_not = [request.GET['ingredient-list' + str(i)] for i in range(6) if
                           request.GET['isPositive' + str(i)] == 'off' and request.GET[
                               'ingredient-list' + str(i)] != '']
        for ingredient in ingredients + ingredients_not:
            try:
                Ingredient.objects.get(ingredient_name=ingredient)
            except Ingredient.DoesNotExist:
                return home(request, error_number=1, missing_ingredient=ingredient)
        difficulty_level = get_difficulty_level(request)
        recipes = Recipe.get_filtered_recipes(ingredients, ingredients_not, request.GET['min-time'],
                                              request.GET['max-time'], difficulty_level)
        if recipes.count() == 0:
            return home(request, error_number=2)
        paginator = Paginator(recipes, 10)
        page = request.GET.get('page', 1)
        recipes = paginator.get_page(page)
        return render(request, 'wyniki.html', {'recipes': recipes, 'last_page': paginator.num_pages})
    except KeyError:
        return home(request, error_number=4)


def update_mark(request):
    recipe_id = request.GET.get("recipe_id")
    mark = int(request.GET.get("mark"))
    if not (1 <= mark <= 5 and isinstance(mark, int)):
        raise ValueError('Mark must be integer between 1 and 5.')
    if recipe_id is None or mark is None or not request.is_ajax():
        return JsonResponse({"ok": False})
    recipe = Recipe.objects.get(id=recipe_id)
    if recipe.amount_of_rates < 0:
        raise ValueError('Amount of rates can\'t be negative')
    recipe.rate = (recipe.rate * recipe.amount_of_rates + mark) / (recipe.amount_of_rates + 1)
    recipe.amount_of_rates += 1
    recipe.save()
    return JsonResponse({"ok": True, "rate": recipe.rate, "amount_of_rates": recipe.amount_of_rates})
