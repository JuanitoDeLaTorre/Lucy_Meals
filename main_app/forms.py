from django.forms import ModelForm
from .models import Ingredient, Recipe

class IngredientForm(ModelForm):
  class Meta:
    model = Ingredient
    fields = '__all__'

class RecipeForm(ModelForm):
  class Meta:
    model = Recipe
    fields = ['name', 'category', 'day_of_week', 'img_url']