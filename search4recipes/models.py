from __future__ import unicode_literals

# for creating and manipulating models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from io_site import settings


class Ingredient(models.Model):
    """
    Model skladnika: tablica skladnikow przepisu
    """
    ingredient_name = models.CharField(_('nazwa'), max_length=250)

    def __init__(self, *args, **kwargs):
        super(Ingredient, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.ingredient_name

    def __str__(self):
        return '{}'.format(self.ingredient_name)

    class Meta:
        verbose_name = _('Składnik')
        verbose_name_plural = _('Składniki')


class Recipe(models.Model):
    """
    Model przepisu: tablica przepisow
    """
    recipe_title = models.CharField(max_length=250, verbose_name=_('Nazwa przepisu'))
    slug = AutoSlugField(_('slug'), populate_from='recipe_title', unique=True)
    image = models.ImageField(_('Zdjęcie przepisu'), blank=True, upload_to=settings.MEDIA_ROOT)
    rate = models.FloatField(_('Ocena'), default=0)
    text = models.TextField(_('Treść przepisu'), default="")
    amount_of_rates = models.IntegerField(_('Ilosc_ocen'), default=0)
    ingredients = models.ManyToManyField(Ingredient, through='search4recipes.IngredientsInRecipes')

    def __unicode__(self):
        return self.recipe_title

    def __str__(self):
        return '{}'.format(self.recipe_title)

    @staticmethod
    def get_by_ingredients(ingredients, ingredients_not=None):
        if ingredients_not is None:
            ingredients_not = list()
        return Recipe.objects.filter(ingredients__ingredient_name__in=ingredients).exclude(
            ingredients__ingredient_name__in=ingredients_not)

    class Meta:
        verbose_name = _('Przepis')
        verbose_name_plural = _('Przepisy')


class Measurement(models.Model):
    """
    Model miar: tablica jednostek miar skladnikow
    """
    unit = models.CharField(max_length=250, unique=True, verbose_name=_('Nazwa'))
    measurement_use = models.CharField(max_length=60, verbose_name=_('Jednostka w przepisie'))

    def __unicode__(self):
        return self.unit

    def __str__(self):
        return format(self.unit)

    class Meta:
        verbose_name = _('Miara')
        verbose_name_plural = _('Miary')


class IngredientsInRecipes(models.Model):
    """
    Model skladnikow w przepisach: tablica przepisow
    """
    ingredient = models.ForeignKey(Ingredient, verbose_name=_('Składnik'), on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, verbose_name=_('Przepis'), on_delete=models.PROTECT)
    measurement = models.ForeignKey(Measurement, verbose_name=_('Miara'), blank=False, null=False,
                                    on_delete=models.PROTECT)
    amount = models.FloatField(_('Ilość'), max_length=200, blank=False, null=False, default=1)

    def __unicode__(self):
        return self.recipe.recipe_title

    def __str__(self):
        return '{} - {}'.format(self.recipe.recipe_title, self.ingredient.ingredient_name)

    def ingredient_formatting(self):
        ingredient_str = self.ingredient.ingredient_name
        return ingredient_str

    def measurement_formatting(self):
        measurement_str = self.measurement.measurement_use
        return measurement_str

    class Meta:
        verbose_name = _('Składnik w przepisie')
        verbose_name_plural = _('Składniki w przepisach')
