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
    img_url = models.URLField(max_length=300, default="https://i.pinimg.com/originals/f4/3d/55/f43d55d69d9e8f11ce20a79277cdfafc.jpg")
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
      return reverse('detail', kwargs={'recipe_id':self.id})
    

class MealPlan(models.Model):
    monday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="monday", null=True, blank=True)
    tuesday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="tuesday", null=True, blank=True)
    wednesday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="wednesday", null=True, blank=True)
    thursday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="thursday", null=True, blank=True)
    friday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="friday", null=True, blank=True)
    saturday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="saturday", null=True, blank=True)
    sunday = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="sunday", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
    