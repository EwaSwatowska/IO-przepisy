from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Recipe, Ingredient


def home(request, missing_ingredient=None):
    ingredients = [x.ingredient_name for x in Ingredient.objects.all()]
    return render(request, 'glowna.html', {"lista": ingredients, 'ingredientNotFound': missing_ingredient})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = [x for x in recipe.ingredientsinrecipes_set.all()]
    return render(request, 'przepis.html', {"przepis": recipe, "skladniki": ingredients})


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
                return home(request, missing_ingredient=ingredient)
        recipes = Recipe.get_by_ingredients(ingredients, ingredients_not)
        paginator = Paginator(recipes, 10)
        page = request.GET.get('page', 1)
        recipes = paginator.get_page(page)
        return render(request, 'wyniki.html', {'recipes': recipes, 'last_page': paginator.num_pages})
    except KeyError:
        return redirect('home')


def update_mark(request):
    recipe_id = request.GET.get("recipe_id")
    mark = float(request.GET.get("mark"))
    if recipe_id is None or mark is None or not request.is_ajax():
        return JsonResponse({"ok": False})
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.rate = (recipe.rate * recipe.amount_of_rates + mark) / (recipe.amount_of_rates + 1)
    recipe.amount_of_rates += 1
    recipe.save()
    return JsonResponse({"ok": True, "rate": recipe.rate, "amount_of_rates": recipe.amount_of_rates})
