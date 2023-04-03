from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('meal_plan/', views.meal_plan, name='meal_plan'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name='detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='create_recipe'),
    path('recipes/<int:pk>/update/',views.RecipeUpdate.as_view(), name='recipes_update'),
    path('recipes/<int:pk>/delete/',views.RecipeDelete.as_view(), name='recipes_delete'),
]
