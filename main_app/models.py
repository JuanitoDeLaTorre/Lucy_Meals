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

CATEGORY = ['Starter/Appetizer','Entree','Dessert','Dessert','Beverage','Side','Baked Good']

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=50, default="banana")
    price = models.IntegerField(default=1)
    calories = models.IntegerField(default=100)
    store = models.CharField(max_length=30, default="Krogers")
    created_at = models.DateTimeField(auto_now_add=True)


class Recipe(models.Model):
    name = models.CharField(max_length=50, default="GABAGOOL")
    category = models.CharField(max_length=50, choices = CATEGORY, default="dessert")
    day_of_week = models.CharField(
        max_length=2, choices=DAYS, default=DAYS[0][0])
    img_url = models.URLField(max_length=250, default="")
    ingredients = models.ManyToManyField(Ingredient)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
