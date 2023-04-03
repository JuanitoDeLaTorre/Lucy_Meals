from django.shortcuts import render
from .models import Recipe, Ingredient
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.


def home(request):
    recipe = Recipe.objects.filter()
    return render(request, 'home.html',
                  {'recipe': recipe}
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


def recipes_detail(request, recipes_id):
    recipe = Recipe.objects.filter(id=recipes_id)
    return render(request, 'detail.html', {
        'recipe': recipe,
    })
