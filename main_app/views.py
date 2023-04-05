from django.shortcuts import render, redirect
from .models import Recipe, Ingredient
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse
from .forms import RecipeForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
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


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['name', 'category', 'day_of_week', 'img_url']
    success_url = '/recipes'

    def from_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# class RecipeUpdate(LoginRequiredMixin, UpdateView):
#     model = Recipe
#     fields = ['name', 'category', 'day_of_week', 'img_url']
#     extra_context = {'recipe': Recipe.objects.filter()}

def recipe_update(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == 'POST':
        recipe_name = request.POST['name']
        recipe_category = request.POST['category']
        recipe_day_of_week = request.POST['day_of_week']
        recipe_img_url = request.POST['img_url']

        recipe.name = recipe_name
        recipe.category = recipe_category
        recipe.day_of_week = recipe_day_of_week
        recipe.img_url = recipe_img_url
        recipe.ingredients.remove()
        
        for key, val in request.POST.items():
            if val == 'on':
                recipe.ingredients.add(Ingredient.objects.filter(name=key)[0].id)
       
        return redirect(reverse('detail', kwargs={"recipe_id": recipe_id}))
    return render(request, 'recipe_update.html', {'recipe': recipe})


class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = '/recipes'


def recipes_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    total_calories = 0
    total_price = 0
    stores = []

    for ing in recipe.ingredients.all():
        total_calories += ing.calories
        total_price += ing.price
        if ing.store not in stores:
            stores.append(ing.store)

    print(total_calories)
    print(total_price)
    print(stores)

    return render(request, 'detail.html', {
        'recipe': recipe, 'calories': total_calories, 'price': total_price, 'stores': stores
    })


def recipes(request):
    all_recipes = Recipe.objects.filter()
    return render(request, 'recipes.html', {'recipes': all_recipes})


@login_required
def recipes_user(request):
    all_recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'recipes_user.html', {'recipes': all_recipes})


@login_required
def meal_plan(request):
    return render(request, 'meal_plan.html')


def get_ingredients(request):
    ingredients = Ingredient.objects.filter()
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
    recipe_user = request.user

    

    new_recipe = Recipe(name=recipe_name, category=recipe_category,
                        day_of_week=recipe_day_of_week, img_url=recipe_img_url, user=recipe_user)
    new_recipe.save()

    # if request.POST['day_of_week'] != "To Be Determined":

    #     match request.POST['day_of_week']:
    #         case 'monday': MealPlan.monday = new_recipe.id

    recipe_obj = Recipe.objects.filter(name=recipe_name)[0]
    # chosen_ingredients = []

    # fetch just ingredients, append to list
    for key, val in request.POST.items():
        if val == 'on':
            recipe_obj.ingredients.add(
                Ingredient.objects.filter(name=key)[0].id)

    # print(chosen_ingredients)

    return redirect('create_recipe')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # link meal plan to user here
            return redirect('/recipes')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
