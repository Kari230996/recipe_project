
from random import sample
from django.db.models.query import QuerySet
from django.forms import BaseModelForm, inlineformset_factory
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from .models import Recipe, RecipeStep, Ingredient, Category
from .forms import DeleteRecipesForm, RecipeForm, RecipeStepForm, IngredientForm, UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.views.generic import FormView



#CRUD
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        all_recipes = Recipe.objects.all()
        shuffled_recipes = sample(list(all_recipes), min(len(all_recipes), 15))
        return shuffled_recipes
  

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['ingredients'] = recipe.ingredients.all()
        context['steps'] = recipe.steps.all()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_create.html'
    success_url = reverse_lazy('recipe_list')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm, extra=1)
        RecipeStepFormSet = inlineformset_factory(Recipe, RecipeStep, form=RecipeStepForm, extra=1)

        if self.request.method == 'POST':
            context['form'] = self.get_form()
            context['ingredient_formset'] = IngredientFormSet(self.request.POST, instance=None)
            context['step_formset'] = RecipeStepFormSet(self.request.POST, self.request.FILES, instance=None)
        else:
            context['form'] = self.get_form()
            context['ingredient_formset'] = IngredientFormSet(instance=None)
            context['step_formset'] = RecipeStepFormSet(instance=None)

        return context
    

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        step_formset = context['step_formset']

        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()
            ingredient_formset.instance = self.object
            step_formset.instance = self.object
            ingredient_formset.save()
            step_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


    
    
class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm, extra=1)
        RecipeStepFormSet = inlineformset_factory(Recipe, RecipeStep, form=RecipeStepForm, extra=1)

        if self.request.method == 'POST':
            context['form'] = self.form_class(self.request.POST, instance=recipe)
            context['ingredient_formset'] = IngredientFormSet(self.request.POST, instance=recipe)
            context['step_formset'] = RecipeStepFormSet(self.request.POST, self.request.FILES, instance=recipe)
        else:
            context['form'] = self.form_class(instance=recipe)
            context['ingredient_formset'] = IngredientFormSet(instance=recipe)
            context['step_formset'] = RecipeStepFormSet(instance=recipe)
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        step_formset = context['step_formset']

        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            self.object = form.save()
            ingredient_formset.save()
            step_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author
    

class RecipeDeleteView(FormView):
    template_name = 'recipes/recipe_confirm_delete.html'
    form_class = DeleteRecipesForm  
    success_url = reverse_lazy('recipe_list') 

    def form_valid(self, form):
        selected_recipes = form.cleaned_data.get('selected_recipes')
        if selected_recipes:

            Recipe.objects.filter(pk__in=selected_recipes).delete()
           
        return super().form_valid(form)

# Other Views
    
class AuthorProfileView(DetailView):
    model = User
    template_name = 'recipes/author_profile.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        context['recipes'] = Recipe.objects.filter(author=author)
        return context



class UserRecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/user_recipe_list.html'
    context_object_name = 'recipes'

    def post(self, request, *args, **kwargs):
        selected_recipes = request.POST.getlist('selected_recipes')
        if selected_recipes:
            Recipe.objects.filter(pk__in=selected_recipes).delete()

        return HttpResponseRedirect(reverse('user_recipe_list'))



class CustomLoginView(LoginView):
    template_name = 'recipes/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('recipe_list')

def category_list(request):
    categories = Recipe.objects.values_list('category', flat=True).distinct()
    return render(request, 'recipes/category_list.html', {'categories': categories})

def category_detail(request, category):
    recipes = Recipe.objects.filter(category=category)
    return render(request, 'recipes/category_detail.html', {'recipes': recipes, 'category': category})


# Other
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login') 
    else:
        form = UserRegistrationForm()
    return render(request, 'recipes/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('recipe_list')
    else:
        form = AuthenticationForm()
    return render(request, 'recipes/login.html', {'form': form, 'user': request.user})


def logout(request):
    auth_logout(request)
    return redirect('recipe_list')





