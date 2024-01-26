from django.db import models

from recipes_api.models import DefaultModel


class Product(DefaultModel):
    used_in_recipes = models.PositiveIntegerField(
        default=0, verbose_name="использовано в рецептах"
    )


class Recipe(DefaultModel):
    product = models.ManyToManyField(Product, through="ProductRecipe")


class ProductRecipe(DefaultModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe"
    )
    weight = models.PositiveIntegerField(
        verbose_name="вес ингредиента в граммах",
    )

    class Meta:
        unique_together = ('product', 'recipe')