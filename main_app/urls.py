from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('meal_plan/', views.meal_plan, name='meal_plan'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name='detail'),
    path('recipes/create/', views.recipe_add_test, name='create_recipe'),
    path('recipes/<int:pk>/update/',views.RecipeUpdate.as_view(), name='recipes_update'),
    path('recipes/<int:pk>/delete/',views.RecipeDelete.as_view(), name='recipes_delete'),
    path('recipes/get_ingredients', views.get_ingredients, name = "get_ingredients"),
    path('create_ingredient', views.create_ingredient, name = "create_ingredient"),
    path('test', views.tester, name = "tester"),
    path('accounts/signup/', views.signup, name='signup'),
]
