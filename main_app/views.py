from django.shortcuts import render, redirect
from .models import Recipe, Ingredient
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse
from .forms import RecipeForm
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
                  {'recipes': recipe, 'appetizers': appetizers, 'dessert': dessert,
                      'entree': entree, 'beverage': beverage, 'side': side, 'bake_good': baked_good}
                  )


class RecipeCreate(CreateView):
    model = Recipe
    fields = ['name', 'category', 'day_of_week', 'img_url']
    success_url = '/recipes'


class RecipeUpdate(UpdateView):
    model = Recipe
    fields = ['name', 'category', 'day_of_week', 'img_url']
   


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = '/recipes'


def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'detail.html', {
        'recipe': recipe,
    })


def recipes(request):
    all_recipes = Recipe.objects.filter()

    return render(request, 'recipes.html', {'recipes': all_recipes})


def meal_plan(request):
    return render(request, 'meal_plan.html')

def get_ingredients(request):
    ingredients = Ingredient.objects.filter()
    return JsonResponse({'ingredients':list(ingredients.values())})

def recipe_add(request):
    recipe_form = RecipeForm()
    return render(request, 'recipe_add.html', {'recipe_form':recipe_form})

def create_ingredient(request):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        calories = request.POST['calories']
        store = request.POST['store']

        new_ingredient = Ingredient(name=name,price=price,calories=calories,store=store)
        new_ingredient.save()

        return HttpResponse('New Ingredient Created Successfully!')

def new_recipe(request):

    recipe_name = request.POST['name']
    recipe_category = request.POST['category']
    recipe_day_of_week = request.POST['day_of_week']
    recipe_img_url = request.POST['img_url']

    new_recipe = Recipe(name=recipe_name,category=recipe_category,day_of_week=recipe_day_of_week,img_url=recipe_img_url)
    new_recipe.save()

    recipe_obj = Recipe.objects.filter(name=recipe_name)[0]
    # chosen_ingredients = []

    #fetch just ingredients, append to list
    for key,val in request.POST.items():
        if val == 'on':
            recipe_obj.ingredients.add(Ingredient.objects.filter(name=key)[0].id)
    
    # print(chosen_ingredients)

    return redirect('create_recipe')