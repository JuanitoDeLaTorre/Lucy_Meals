from django.shortcuts import render
from .models import Recipe, Ingredient
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.


def home(request):
    recipe = Recipe.objects.filter()

    appetizers = Recipe.objects.filter(category='Appetizer')
    entree = Recipe.objects.filter(category='Entree')
    dessert = Recipe.objects.filter(category='Dessert')
    beverage = Recipe.objects.filter(category='Beverage')
    side = Recipe.objects.filter(category='Side')
    baked_good = Recipe.objects.filter(category='Baked Good')

    return render(request, 'home.html',
                  {'recipes': recipe, 'appetizers': appetizers, 'dessert': dessert, 'entree': entree, 'beverage': beverage, 'side': side, 'bake_good':baked_good}
                  )

# def create_recipe(request):
#     return render(request, 'create_recipe.html')


class RecipeCreate(CreateView):
    model = Recipe
    fields = ['name', 'category', 'day_of_week', 'img_url']
    success_url = '/recipes'


def meal_plan(request):
    return render(request, 'meal_plan.html')


def recipes(request):
    all_recipes = Recipe.objects.filter()

    return render(request, 'recipes.html', {'recipes':all_recipes})


def recipes_detail(request, recipe_id):
    print("HITTING ROUTE!")
    recipe = Recipe.objects.filter(id=recipe_id)
    return render(request, 'detail.html', {
        'recipe': recipe,
    })
