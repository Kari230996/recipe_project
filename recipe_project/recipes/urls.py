from django.urls import path
from . import views
from .views import UserRecipeListView, AuthorProfileView, category_list, category_detail

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/new/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe_delete'),
    path('my-recipes/', UserRecipeListView.as_view(), name='user_recipe_list'),
    path('author/<int:pk>/', AuthorProfileView.as_view(), name='author_profile'),
    path('categories/', category_list, name='category_list'),
    path('category/<str:category>/', category_detail, name='category_detail')

]