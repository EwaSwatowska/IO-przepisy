from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Przepis, Skladnik, Miara, SkladnikiwPrzepisach
from .serializers import RecipeSerializer, IngredientSerializer, IngInRecSerializer, MeasurmentSerializer


class IndexView(APIView):
    """
    API view for searching Recipes
    """
    allowed_methods = ['GET']
    serializer_class = RecipeSerializer


def get(self, request, *args, **kwargs):
    queryset = Przepis.objects.all()

    # filtering recipes by name
    name = request.query_params.get('name', None)
    if name is not None:
        queryset = queryset.filter(name__icontains=name)

    serializer = self.serializer_class(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class PrzepisViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Recipes to be viewed or edited.
    """
    queryset = Przepis.objects.all().order_by('nazwa_przepisu')
    serializer_class = RecipeSerializer


class SkladnikViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ingredients to be viewed or edited.
    """
    queryset = Skladnik.objects.all()
    serializer_class = IngredientSerializer


class MiaraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows measurements to be viewed or edited.
    """
    queryset = Miara.objects.all()
    serializer_class = MeasurmentSerializer


class SkladnikiWPrzepisachViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows whole recipes to be viewed or edited.
    """
    queryset = SkladnikiwPrzepisach.objects.all()
    serializer_class = IngInRecSerializer


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


def home(request):
    skladniki = [x.nazwa_produktu for x in Skladnik.objects.all()]
    return render(request, 'glowna.html', {"lista": skladniki})


def recipe_detail(request, recipeid):
    recipe = Przepis.objects.get(id=recipeid)
    skladniki = [x for x in recipe.skladnikiwprzepisach_set.all()]
    return render(request, 'przepis.html', {"przepis": recipe, "skladniki": skladniki})


def recipe_list(request):
    ingredients = [request.POST['lista-skladnikow' + str(i)] for i in range(6) if
                   request.POST['isPositive' + str(i)] == 'on' and request.POST['lista-skladnikow' + str(i)] != '']
    ingredients_not = [request.POST['lista-skladnikow' + str(i)] for i in range(6) if
                       request.POST['isPositive' + str(i)] == 'off' and request.POST['lista-skladnikow' + str(i)] != '']
    for ingredient in ingredients + ingredients_not:
        try:
            Skladnik.objects.get(nazwa_produktu=ingredient)
        except Skladnik.DoesNotExist:
            return render(request, 'glowna.html', {'ingredientNotFound': ingredient})
    przepisy = Przepis.get_by_ingredients(ingredients, ingredients_not)
    paginator = Paginator(przepisy, 10)
    page = request.GET.get('page', 1)
    przepisy = paginator.get_page(page)
    return render(request, 'wyniki.html', {'przepisy': przepisy})
