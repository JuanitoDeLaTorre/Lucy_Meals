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

    appetizers = Recipe.objects.filter(category='App')
    entree = Recipe.objects.filter(category='En')
    dessert = Recipe.objects.filter(category='D')
    beverage = Recipe.objects.filter(category='Bev')
    side = Recipe.objects.filter(category='S')
    baked_good = Recipe.objects.filter(category='Ba')


    return render(request, 'recipes.html', {'recipes':all_recipes})


def recipes_detail(request, recipes_id):
    recipe = Recipe.objects.filter(id=recipes_id)
    return render(request, 'detail.html', {
        'recipe': recipe,
    })
