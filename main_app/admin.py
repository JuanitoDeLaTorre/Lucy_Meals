from django.contrib import admin
from .models import Recipe, Ingredient, MealPlan

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(MealPlan)
# Register your models here.
