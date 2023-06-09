from django.shortcuts import render, redirect
from .models import Recipe, Ingredient, MealPlan, User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse
from .forms import RecipeForm, CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
import json


def home(request):
    recipe = Recipe.objects.filter()
    print(request.user)
    if request.user.is_authenticated:
        meal_plan = MealPlan.objects.filter(user=request.user).first()
    else:
        meal_plan = False
    appetizers = len(list(Recipe.objects.filter(category='Appetizer')))
    entree = len(list(Recipe.objects.filter(category='Entree')))
    dessert = len(list(Recipe.objects.filter(category='Dessert')))
    beverage = len(list(Recipe.objects.filter(category='Beverage')))
    side = len(list(Recipe.objects.filter(category='Side')))
    baked_good = len(list(Recipe.objects.filter(category='Baked Good')))
    print(baked_good)

    return render(request, 'home.html',
                  {'recipes': recipe, 'appetizers': appetizers, 'dessert': dessert,
                      'entree': entree, 'beverage': beverage, 'side': side, 'bake_good': baked_good, 'meal_plan':meal_plan}
                  )


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['name', 'category', 'day_of_week', 'img_url']
    success_url = '/recipes'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def recipe_update(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if request.method == 'POST':
        recipe_name = request.POST['name']
        recipe_category = request.POST['category']
        recipe_day_of_week = request.POST['day_of_week']
        recipe_img_url = request.POST['img_url']
        recipe_instructions = request.POST['instructions']

        recipe.name = recipe_name
        recipe.category = recipe_category
        recipe.day_of_week = recipe_day_of_week
        recipe.img_url = recipe_img_url
        recipe.instructions = recipe_instructions
        recipe.ingredients.clear()

        for key, val in request.POST.items():
            if val == 'on':
                recipe.ingredients.add(
                    Ingredient.objects.filter(name=key)[0].id)
        recipe.save()

        return redirect(reverse('detail', kwargs={"recipe_id": recipe_id}))
    return render(request, 'recipe_update.html', {'recipe': recipe})


class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = '/recipes/all'


def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    total_calories = 0
    total_price = 0
    stores = []
    search_string = "https://www.google.com/search?q="

    for ing in recipe.ingredients.all():
        total_calories += ing.calories
        total_price += ing.price
        if ing.store not in stores:
            stores.append(ing.store)
    
    #append words to google search query base URL with '+' in between
    for word in recipe.name.split(' '):
        search_string += word
        search_string += '+'
    
    #remove last + from search_string
    search_string = search_string.rstrip(search_string[-1])
    

    return render(request, 'detail.html', {
        'recipe': recipe, 'calories': total_calories, 'price': total_price, 'stores': stores, 'search_string':search_string
    })


def recipes(request, recipe_category):

    #if the serach category isn't 'all', filter recipes by user-defined category
    if recipe_category != "all":
        recipes = Recipe.objects.filter(category=recipe_category.capitalize())
    else:
        recipes = Recipe.objects.filter()

    return render(request, 'recipes.html', {'recipes': recipes})


@login_required
def recipes_user(request):
    all_recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'recipes_user.html', {'recipes': all_recipes})


@login_required
def meal_plan(request):
    meal_plan = MealPlan.objects.filter(user=request.user).first()

    days = {'monday':meal_plan.monday, 'tuesday': meal_plan.tuesday, 'wednesday': meal_plan.wednesday, 
            'thursday': meal_plan.thursday, 'friday': meal_plan.friday, 'saturday': meal_plan.saturday, 'sunday': meal_plan.sunday}
    calories = {}
    calories_temp = 0

    #loop through all days in meal_plan (days dict) and add up calories for each day/assign to dict
    for name, day in days.items():
        calories_temp = 0
        if day:
            for item in day.ingredients.all():
                calories_temp += item.calories
            calories[name] = calories_temp

    return render(request, 'meal_plan.html', {'meal_plan':meal_plan, 'calories': calories})


def meal_add(request):
    recipes =  Recipe.objects.filter()
    current_meals = MealPlan.objects.filter(user=request.user)[0]
    recipe_day_of_week = request.POST.get('day_of_week')
    new_recipe = Recipe.objects.filter(name=request.POST.get('recipes')).first()

    if request.method == 'POST':
        if recipe_day_of_week == 'Monday':
            current_meals.monday = new_recipe
        elif recipe_day_of_week == 'Tuesday':
            current_meals.tuesday = new_recipe
        elif recipe_day_of_week == 'Wednesday':
            current_meals.wednesday = new_recipe
        elif recipe_day_of_week == 'Thursday':
            current_meals.thursday = new_recipe
        elif recipe_day_of_week == 'Friday':
            current_meals.friday = new_recipe
        elif recipe_day_of_week == 'Saturday':
            current_meals.saturday = new_recipe
        elif recipe_day_of_week == 'Sunday':
            current_meals.sunday = new_recipe
        current_meals.save()
        return redirect(reverse('meal_plan'))
        
    return render(request, 'meal_add.html',{'recipes': recipes, 'current_meals': current_meals})


def get_ingredients(request):
    ingredients = Ingredient.objects.all()
    
    if request.method == 'POST':
        recipe_ingredients = []

        #loop through all the ingredients in the incoming recipe and append names to the outgoing JSON response object
        for ing in list(Recipe.objects.get(id=request.POST.get('recipe_id','')).ingredients.all()):
            recipe_ingredients.append(ing.name)
        
        return JsonResponse({'ingredients': list(ingredients.values()), 'recipe_ingredients': recipe_ingredients})

    return JsonResponse({'ingredients': list(ingredients.values())})



def recipe_add(request):
    recipe_form = RecipeForm()
    return render(request, 'recipe_add.html', {'recipe_form': recipe_form})


def create_ingredient(request):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        calories = request.POST['calories']
        store = request.POST['store']

        new_ingredient = Ingredient(
            name=name, price=price, calories=calories, store=store)
        new_ingredient.save()

        return HttpResponse('New Ingredient Created Successfully!')


def new_recipe(request):

    recipe_name = request.POST['name']
    recipe_category = request.POST['category']
    recipe_day_of_week = request.POST['day_of_week']
    recipe_img_url = request.POST['img_url']
    recipe_instructions = request.POST['instructions']
    recipe_user = request.user

    new_recipe = Recipe(name=recipe_name, category=recipe_category,
                        day_of_week=recipe_day_of_week, img_url=recipe_img_url, instructions=recipe_instructions, user=recipe_user)
    new_recipe.save()

    recipe_obj = Recipe.objects.filter(name=recipe_name)[0]

    # fetch ingredients from POST, associate with recipe from request
    for key, val in request.POST.items():
        if val == 'on':
            recipe_obj.ingredients.add(
                Ingredient.objects.filter(name=key)[0].id)
            
    #fetch current meal plan
    current_meals = MealPlan.objects.filter(user=request.user)[0]

    if recipe_day_of_week == 'Monday':
        current_meals.monday = new_recipe
    elif recipe_day_of_week == 'Tuesday':
        current_meals.tuesday = new_recipe
    elif recipe_day_of_week == 'Wednesday':
        current_meals.wednesday = new_recipe
    elif recipe_day_of_week == 'Thursday':
        current_meals.thursday = new_recipe
    elif recipe_day_of_week == 'Friday':
        current_meals.friday = new_recipe
    elif recipe_day_of_week == 'Saturday':
        current_meals.saturday = new_recipe
    elif recipe_day_of_week == 'Sunday':
        current_meals.sunday = new_recipe
    current_meals.save()

    return redirect('create_recipe')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # link meal plan to user here
            meal_plan = MealPlan(user=request.user)
            meal_plan.save()
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = CustomUserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def search_recipes(request):
    if request.method == "POST":
        searched = request.POST['searched'].lower()
        categories = ['appetizer', 'entree', 'dessert', 'beverage', 'side', 'baked Good']
        all_ingredients = []
        query_recipes_ing = []

        #fetch the names of all ingredients for matching
        for ing in Ingredient.objects.all():
            all_ingredients.append(ing.name)

        if searched.capitalize() in all_ingredients:
            #for all recipes in the database, loop through each one's ingredients to check for matches
            #append to list if it matches
            for recipe in Recipe.objects.all():
                for ing in recipe.ingredients.all():
                    if searched.capitalize() == ing.name:
                        query_recipes_ing.append(recipe)
            
            return render (request, 'search_recipes.html',
                        {'searched' : request.POST['searched'], 'recipes': query_recipes_ing})

        if searched in categories:
            recipes = list(Recipe.objects.filter(category=searched.capitalize()))
        else:
            recipes = list(Recipe.objects.filter(name__icontains=searched))
        return render (request, 'search_recipes.html',
                       {'searched' : request.POST['searched'], 'recipes': recipes})
    else:
        return render (request, 'search_recipes.html',
                       {})
    