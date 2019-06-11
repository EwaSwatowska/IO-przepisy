# Autorzy: Karolina Cibor, Paweł Goliszewski
from django.urls import path

from . import views

urlpatterns = [
    path('recipe/<int:recipe_id>/', views.recipe_detail, name="recipe_detail"),
    path('recipe_list/', views.recipe_list, name="recipe_list"),
    path('ajax/update_mark', views.update_mark, name="update_mark"),
    path('', views.home, name="home"),
]
