from django.conf import settings
from django.db.models import F
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.request import Request
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from api.serializers import ProductSerializer, RecipeSerializer
from recipes.models import Product, ProductRecipe, Recipe


def cook_recipe(request: Request, recipe_id: int) -> JsonResponse:
    """
    Функция для приготовления рецепта.

     Увеличивает счетчик поля 'used_in_recipes' на единицу для каждого
     продукта в рецепте. Возвращает сериализованные продукты с обновленным
     счечтиком поля и сообщением о приготовлении по рецепту.

    Args:
        request: HttpRequest объект.
        recipe_id: ID рецепта, по которому готовят.

    Returns:
        Response: Возвращает JSON с сериализованными продуктами и сообщением.

    Raises:
        Http404: Если запрашиваемого рецепта нет.
    """
    recipe = get_object_or_404(Recipe, id=recipe_id)
    products = Product.objects.filter(recipe=recipe)
    products.update(
        used_in_recipes=F("used_in_recipes") + 1
    )  # Обеспечивает атомарность операции. # noqa
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(
        {
            "message": "Рецепт был изготовлен из продуктов ниже:",
            "products": serializer.data,
        },
        status=HTTP_201_CREATED,
        json_dumps_params={
            "ensure_ascii": False
        },  # Для корректного отображения текста в браузере # noqa
    )


def add_to_recipe(
    request: Request, recipe_id: int, product_id: int, weight: int
) -> JsonResponse:
    """
    Функция для добавления изменений в рецепт.

     Добавляет продукт в рецепт, если такого не было и обновляет вес в граммах.

    Args:
        request: HttpRequest объект.
        recipe_id: ID рецепта, который обновляют.
        product_id: ID продукта, который изменяют/добавляют.
        weight: Вес продукта.

    Returns:
        JsonResponse: Возвращает JSON с сериализованными рецептом и сообщением.

    Raises:
        Http404: Если запрашиваемого рецпта и/или продукта нет.
        Не принимает нулевый вес продукта.
    """
    if weight <= 0:
        return JsonResponse(
            {"error": f"Weight должен быть больше {settings.MINIMAL_WEIGHT}."},
            status=HTTP_400_BAD_REQUEST,
        )
    recipe = get_object_or_404(Recipe, id=recipe_id)
    product = get_object_or_404(Product, id=product_id)
    product_recipe, created = ProductRecipe.objects.get_or_create(
        recipe=recipe, product=product, defaults={"weight": weight}
    )
    if not created:
        product_recipe.weight = weight
        product_recipe.save()
    serializer = RecipeSerializer(recipe)
    return JsonResponse(
        {"message": "Рецепт успешно изменен", "recipe": serializer.data},
        json_dumps_params={"ensure_ascii": False},
        status=HTTP_201_CREATED,
    )


def recipes_without_product(
    request: HttpRequest, product_id: int
) -> HttpResponse:
    """
    Функция для отображения всех рецептов без указанного продукта.

    Так же включает рецепты с, если кол-во продукта в рецепте
    не больше установлленого в настройках значения.

    Args:
        request: HttpRequest объект.
        product_id: ID продукта, который исключают.

    Returns:
        Response: Возвращает HttpResponse.

    Raises:
        Http404: Если запрашиваемого продукта нет в базе.
        Не принимает нулевый вес продукта.
    """
    product = get_object_or_404(Product, id=product_id)
    excluded_recipe_ids = ProductRecipe.objects.filter(
        product=product, weight__gt=settings.MAX_WEIGHT_TO_IGNORE
    ).values("recipe_id")
    recipes = Recipe.objects.exclude(id__in=excluded_recipe_ids)
    context = {
        "recipes": recipes,
        "exclude": product,
    }
    return render(request, "recipes/recipes_without.html", context)
