from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from .models import Recipe, Ingredient


def home(request):
    skladniki = [x.ingredient_name for x in Ingredient.objects.all()]
    return render(request, 'glowna.html', {"lista": skladniki})


def recipe_detail(request, recipeid):
    recipe = Recipe.objects.get(id=recipeid)
    skladniki = [x for x in recipe.ingredientsinrecipes_set.all()]
    return render(request, 'przepis.html', {"przepis": recipe, "skladniki": skladniki})


def recipe_list(request):
    ingredients = [request.POST['lista-skladnikow' + str(i)] for i in range(6) if
                   request.POST['isPositive' + str(i)] == 'on' and request.POST['lista-skladnikow' + str(i)] != '']
    ingredients_not = [request.POST['lista-skladnikow' + str(i)] for i in range(6) if
                       request.POST['isPositive' + str(i)] == 'off' and request.POST['lista-skladnikow' + str(i)] != '']
    for ingredient in ingredients + ingredients_not:
        try:
            Ingredient.objects.get(ingredient_name=ingredient)
        except Ingredient.DoesNotExist:
            return render(request, 'glowna.html', {'ingredientNotFound': ingredient})
    przepisy = Recipe.get_by_ingredients(ingredients, ingredients_not)
    paginator = Paginator(przepisy, 10)
    page = request.GET.get('page', 1)
    przepisy = paginator.get_page(page)
    return render(request, 'wyniki.html', {'recipes': przepisy})


def update_mark(request):
    recipe_id = request.GET.get("recipe_id")
    mark = float(request.GET.get("mark"))
    if recipe_id is None or mark is None or not request.is_ajax():
        return JsonResponse({"ok": False})
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.mark = (recipe.mark * recipe.amount_of_marks + mark) / (recipe.amount_of_marks + 1)
    recipe.amount_of_marks += 1
    recipe.save()
    return JsonResponse({"ok": True, "mark": recipe.mark, "amount_of_marks": recipe.amount_of_marks})
