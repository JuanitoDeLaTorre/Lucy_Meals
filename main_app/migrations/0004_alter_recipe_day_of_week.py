# Generated by Django 4.1.7 on 2023-04-04 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_ingredient_calories_alter_ingredient_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='day_of_week',
            field=models.CharField(choices=[('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('Th', 'Thursday'), ('F', 'Friday'), ('Sa', 'Saturday'), ('S', 'Sunday')], default='M', max_length=2),
        ),
    ]