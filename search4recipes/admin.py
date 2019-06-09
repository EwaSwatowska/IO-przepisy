# Register your models here.
from django.contrib import admin

from .models import Measurement, IngredientsInRecipes, Recipe, Ingredient

admin.site.register(Ingredient)
admin.site.register(Measurement)
admin.site.register(IngredientsInRecipes)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('recipe_title', 'difficulty_level', 'preparation_time', 'image', 'text',)
