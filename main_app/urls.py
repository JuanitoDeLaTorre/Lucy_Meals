from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='create_recipe'),
    path('meal_plan/', views.meal_plan, name='meal_plan'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipe/<int:recipe_id>/', views.recipes_detail, name='detail'),
]
