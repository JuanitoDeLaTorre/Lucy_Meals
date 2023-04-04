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
    day_of_week = models.CharField(max_length=255, default ="Monday")
    img_url = models.URLField(max_length=300, default="")
    ingredients = models.ManyToManyField(Ingredient)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
      return reverse('detail', kwargs={'recipe_id':self.id})
    