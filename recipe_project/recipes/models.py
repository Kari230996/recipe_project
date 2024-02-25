from django.db import models
from django.conf import settings
from django.urls import reverse

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category_choices = [
        ('Sauce', 'Sauce recipes'),
        ('Sweets', 'Sweets recipes'),
        ('Seasoning', 'Seasoning recipes'),
        ('Drink', 'Drink Recipes'),
        ('Marinade', 'Marinade recipes'),
        ('Dough', 'Recipes for dough products'),
        ('Snack', 'Snack Recipes'),
        ('Preparation', 'Preparation recipes'),
        ('Main course', 'Main course recipes'),
        ('First course', 'First course recipes'),
    ]
    category = models.CharField(max_length=100, choices=category_choices)
    cooking_time = models.CharField(max_length=50)
    image = models.ImageField(upload_to='recipe_images/')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})
    
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=50)
    quantity = models.FloatField()
    unit_choices = [
        ('.', '.'),
        ('cups', 'cups'),
        ('ml', 'ml'),
        ('l', 'l'),
        ('g', 'g'),
        ('kg', 'kg'),
        ('tsp.', 'tsp.'),
        ('ssp.', 'ssp.'),
        ('pc.', 'pc.'),
        ('taste', 'taste')
    ]
    unit = models.CharField(max_length=10, choices=unit_choices, default='cups')
    
    def __str__(self):
        return self.name


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_step_images/', blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name






