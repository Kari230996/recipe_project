from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Category, Ingredient, RecipeStep
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['recipe', 'name', 'quantity', 'unit']

class RecipeStepForm(forms.ModelForm):
    class Meta:
        model = RecipeStep
        fields = ['description', 'image']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget = forms.Select(choices=Recipe.category_choices)


IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm, extra=1)
RecipeStepFormSet = inlineformset_factory(Recipe, RecipeStep, form=RecipeStepForm, extra=1, can_delete=True)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data
    

class DeleteRecipesForm(forms.Form):
    selected_recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Select recipes to delete'
    )