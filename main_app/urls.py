from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('meal_plan/', views.meal_plan, name='meal_plan'),
    path('meal_plan/meal_add/', views.meal_add, name='meal_add'),
    # path('meal_plan/meal_update_plan/', views.meal_plan_update, name='meal_plan_update')
    path('recipes/<recipe_category>', views.recipes, name='recipes'),
    path('recipes/user/', views.recipes_user, name='recipes_user'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name='detail'),
    path('recipes/create/', views.recipe_add, name='create_recipe'),
    path('recipes/new_recipe/', views.new_recipe, name='new_recipe'),
    path('recipes/<int:recipe_id>/update/', views.recipe_update, name='recipes_update'),
    path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipes_delete'),
    path('recipes/get_ingredients/', views.get_ingredients, name="get_ingredients"),
    path('create_ingredient/', views.create_ingredient, name="create_ingredient"),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name='reset_password'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_complete'),
    path('search_recipes/', views.search_recipes, name='search_recipes')
]
