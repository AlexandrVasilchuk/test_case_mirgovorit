from rest_framework import serializers

from recipes.models import Product, ProductRecipe, Recipe


class ProductRecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name")

    class Meta:
        model = ProductRecipe
        fields = ("name", "weight")


class RecipeSerializer(serializers.ModelSerializer):
    product = ProductRecipeSerializer(many=True, source="recipe")

    class Meta:
        model = Recipe
        fields = ("name", "product")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "used_in_recipes",
        )
