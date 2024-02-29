from django.contrib import admin
from .models import Ingredient, Recipe, Category, RecipeStep

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, RecipeStepInline]
    list_display = ['title'] 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    pass
