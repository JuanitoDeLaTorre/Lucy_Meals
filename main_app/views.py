from django.shortcuts import render
from .models import Recipe, Ingredient
# Create your views here.

def home(request):
    recipe = Recipe.objects.filter()
    return render(request, 'home.html', 
        {'recipe':recipe}
    )

def create_recipe(request):
    return render(request, 'create_recipe.html')

def meal_plan(request):
    return render(request, 'meal_plan.html')

def recipes(request):
    return render(request, 'recipes.html')

def recipes_detail(request, recipes_id):
    recipe = Recipe.objects.filter(id=recipes_id)
    return render(request, 'detail.html',{
        'recipe': recipe,
    })