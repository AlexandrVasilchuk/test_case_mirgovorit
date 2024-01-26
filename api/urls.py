from django.urls import path

from api.views import add_to_recipe, cook_recipe, recipes_without_product

urlpatterns = [
    path("cook_recipe/<int:recipe_id>/", cook_recipe),
    path(
        "add_product/<int:recipe_id>/<int:product_id>/<int:weight>/",
        add_to_recipe,
    ),
    path(
        "show_recipes_without_product/<int:product_id>/",
        recipes_without_product,
    ),
]
