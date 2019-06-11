from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from io_site import settings


class Ingredient(models.Model):
    """
    Model skladnika: tablica skladnikow przepisu
    """
    ingredient_name = models.CharField(_('nazwa'), max_length=250)

    def __init__(self, *args, **kwargs):
        super(Ingredient, self).__init__(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.ingredient_name)

    class Meta:
        verbose_name = _('Składnik')
        verbose_name_plural = _('Składniki')


class Recipe(models.Model):
    """
    Model przepisu: tablica przepisow
    """
    DIFFICULTY_CHOICES = ((0, _("Łatwy")), (1, _("Średni")), (2, _("Trudny")))
    recipe_title = models.CharField(max_length=250, verbose_name=_('Nazwa przepisu'), unique=True)
    image = models.ImageField(_('Zdjęcie przepisu'), blank=True, upload_to=settings.IMAGE_DIR)
    rate = models.FloatField(_('Ocena'), default=0)
    text = models.TextField(_('Treść przepisu'), default="", help_text='Użyj &lt;br&gt; aby przejść do nowje linii.')
    amount_of_rates = models.IntegerField(_('Ilość ocen'), default=0)
    preparation_time = models.IntegerField(_('Czas przygotowania'), default=10,
                                           help_text="Czas przygotowania w minutach")
    difficulty_level = models.IntegerField(_('Poziom trudności'), choices=DIFFICULTY_CHOICES, default=1)
    ingredients = models.ManyToManyField(Ingredient, through='search4recipes.IngredientsInRecipes')

    def __str__(self):
        return '{}'.format(self.recipe_title)

    @staticmethod
    def get_filtered_recipes(ingredients=None, ingredients_not=None, min_time: int = None, max_time: int = None,
                             difficulty_level: int = None):
        """
        Metoda służąca do odfiltrowania wyników przepisów. Brak filtrów zwróci wszystkie przepisy
        :param ingredients: lista składników, które muszą być wykorzystane w przepise
        :param ingredients_not: lista składników, które nie mogą pojawić się w przepisie
        :param min_time: minimalny czas przygotowania potrawy
        :param max_time: maksymalny czas przygotowania potrawy
        :param difficulty_level: poziom trudności potrawy
        :return:
        """
        if ingredients is None:
            ingredients = list()
        if ingredients_not is None:
            ingredients_not = list()
        result = Recipe.objects.all()
        for ingredient in ingredients:
            result = result.filter(ingredients__ingredient_name__exact=ingredient)
        result = result.exclude(ingredients__ingredient_name__in=ingredients_not)
        if min_time is not None:
            result = result.filter(preparation_time__gte=min_time)
        if max_time is not None:
            result = result.filter(preparation_time__lte=max_time)
        if difficulty_level is not None:
            result = result.filter(difficulty_level__exact=difficulty_level)
        return result.order_by('id')

    def get_difficuty_level_name(self):
        for x in self.DIFFICULTY_CHOICES:
            if x[0] == self.difficulty_level:
                return x[1]

    class Meta:
        verbose_name = _('Przepis')
        verbose_name_plural = _('Przepisy')


class Measurement(models.Model):
    """
    Model miar: tablica jednostek miar skladnikow
    """
    unit = models.CharField(max_length=250, unique=True, verbose_name=_('Nazwa'))
    measurement_use = models.CharField(max_length=60, verbose_name=_('Jednostka w przepisie'))

    def __str__(self):
        return format(self.unit)

    class Meta:
        verbose_name = _('Miara')
        verbose_name_plural = _('Miary')


class IngredientsInRecipes(models.Model):
    """
    Model skladnikow w przepisach: zapewnia realcję wiele-do-wielu w pomiędzy przepisami a składnikami
    """
    ingredient = models.ForeignKey(Ingredient, verbose_name=_('Składnik'), on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, verbose_name=_('Przepis'), on_delete=models.PROTECT)
    measurement = models.ForeignKey(Measurement, verbose_name=_('Miara'), blank=False, null=False,
                                    on_delete=models.PROTECT)
    amount = models.FloatField(_('Ilość'), max_length=200, blank=False, null=False, default=1)

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
