from django.contrib import admin

from recipes.models import Product, ProductRecipe, Recipe


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"


class ProductRecipeAdmin(admin.TabularInline):
    model = ProductRecipe
    readonly_fields = ("name",)


@admin.register(Recipe)
class RecipeAdmin(BaseAdmin):
    list_display = ("pk", "name")
    list_editable = ("name",)
    search_fields = ("name",)
    inlines = (ProductRecipeAdmin,)


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ("pk", "name", "used_in_recipes")
    search_fields = ("name",)
    readonly_fields = ("used_in_recipes",)
