from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Przepis, Skladnik, Miara, SkladnikiwPrzepisach
from .serializers import RecipeSerializer, IngredientSerializer, IngInRecSerializer,MeasurmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth import authenticate,login
from rest_framework import viewsets, status
from django.template.context_processors import csrf


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



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


def home(request):
    return render(request, 'home.html')

def recipe_detail(request):
    return render(request, 'recipes/recipe_detail.html')

def recipe_list(request):
    return render(request, 'recipes/recipe_list.html')

def login(request):
    c={}
    c.update(csrf(request))
    return render(request,'registration/login.html',c)

def auth_view(request):
    username=request.POST.get('username', '')
    password=request.POST.get('password', '')
    user=auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('registration/loggedin')
    else:
        return HttpResponseRedirect('registration/invalid_login')
"""
def loggedin(request):
    username = request.GET.get("username")
    return  render(request, "registration/loggedin.html", {"full_name": username})

def logout(request):
    auth.logout(request)
    pass

def invalid_login(request):
    return render('registration/invalid_login.html')
"""