from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

DAYS = (
    ('M', 'Monday'),
    ('T', 'Tuesday'),
    ('W', 'Wednesday'),
    ('Th', 'Thursday'),
    ('F', 'Friday'),
    ('Sa', 'Saturday'),
    ('S', 'Sunday'),
    ('TBD', 'To Be Determined')
)

CATEGORY = (
    ('Appetizer', 'Appetizer'),
    ('Entree', 'Entree'),
    ('Dessert', 'Dessert'),
    ('Beverage', 'Beverage'),
    ('Side', 'Side'),
    ('Baked Good', 'Baked Good'),
)




class Ingredient(models.Model):
    name = models.CharField(max_length=50, default="banana")
    price = models.DecimalField(default=1, decimal_places=2, max_digits=5)
    calories = models.IntegerField(default=1)
    store = models.CharField(max_length=30, default="Krogers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100, default="GABAGOOL")
    category = models.CharField(max_length=100, choices = CATEGORY, default="App")
    day_of_week = models.CharField(max_length=255, choices=DAYS, default ="To Be Determined")
    img_url = models.URLField(max_length=300, default="")
    ingredients = models.ManyToManyField(Ingredient)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
      return reverse('detail', kwargs={'recipe_id':self.id})
    

class MealPlan(models.Model):
    monday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="monday", default = None)
    tuesday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="tuesday", default = None)
    wednesday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="wednesday", default = None)
    thursday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="thursday", default = None)
    friday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="friday", default = None)
    saturday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="saturday", default = None)
    sunday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="sunday", default = None)

    def __str__(self):
        return self.name
    