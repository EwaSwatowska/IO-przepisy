from rest_framework import serializers
from .models import Przepis, Skladnik, Miara, SkladnikiwPrzepisach


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for Ingredient model
    """

    class Meta:
        model = Skladnik
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for Recipe model
    """

    class Meta:
        model = Przepis
        fields = '__all__'


class MeasurmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Measurement model
    """

    class Meta:
        model = Miara
        fields = '__all__'


class IngInRecSerializer(serializers.ModelSerializer):
    """
    Serializer for Ingredients in Recipe model
    """
    skladnik = IngredientSerializer(many=True)
    przepis = RecipeSerializer(many=True)
    maiara = MeasurmentSerializer(many=True)

    class Meta:
        model = SkladnikiwPrzepisach
        fields = '__all__'  # ('', '', '', '', '')
