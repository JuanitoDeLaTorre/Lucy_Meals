from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('meal_plan/', views.meal_plan, name='meal_plan'),
    path('meal_plan/meal_add/', views.meal_add, name = 'meal_add'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/user/', views.recipes_user, name='recipes_user'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name='detail'),
    path('recipes/create/', views.recipe_add, name='create_recipe'),
    path('recipes/new_recipe/', views.new_recipe, name='new_recipe'),
    path('recipes/<int:recipe_id>/update/',views.recipe_update, name='recipes_update'),
    path('recipes/<int:pk>/delete/',views.RecipeDelete.as_view(), name='recipes_delete'),
    path('recipes/get_ingredients', views.get_ingredients, name = "get_ingredients"),
    path('create_ingredient', views.create_ingredient, name = "create_ingredient"),
    path('accounts/signup/', views.signup, name='signup'),
]
