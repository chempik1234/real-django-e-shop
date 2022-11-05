from django.db import models
import os
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


# class Cart(models.Model):
#     user_id = models.IntegerField(unique=True)
#
#
# class CartAndProduct(models.Model):
#     order_id = models.IntegerField


class Opinion(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(null=True,max_length=1200)
    image = models.ImageField(null=True, blank=True, upload_to='opinion')
    pr_table = models.CharField(null=True,max_length=255)  # tomato_seeds
    pr_id = models.IntegerField(null=True)

    class Meta:
        db_table = "opinion"


class Product(models.Model):
    title = models.CharField(null=False, max_length=255, default="DEFAULT NAME12345")
    image = None #models.ImageField(upload_to=os.path.join(os.curdir, '../static/img/product_img'))
    description = models.CharField(null=True, max_length=500)
    price = models.IntegerField(null=False, default=1, validators=[MinValueValidator(1)])

    class Meta:
        abstract = True


class Rates(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(null=False, default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    pr_table = models.CharField(null=True,max_length=255)  # tomato_seeds
    pr_id = models.IntegerField(null=True)

    class Meta:
        db_table = "rates"


### СЕМЕНА
class SeedsCategories(models.Model):
    name = models.CharField(null=False, max_length=50)

    class Meta:
        db_table = "seed_categories"


class RipeningPeriods(models.Model):
    name = models.CharField(null=False, max_length=50)

    class Meta:
        db_table = "ripening_periods"


class SimpleSeeds(models.Model):
    category = models.ForeignKey(SeedsCategories, on_delete=models.CASCADE, default=1)
    ripening_period = models.ForeignKey(RipeningPeriods, on_delete=models.CASCADE, default=1)
    ripe_color = models.CharField(null=True, max_length=30)
    ripe_form = models.CharField(null=True, max_length=50)
    ripe_weight_grams = models.IntegerField(null=True)
    yield_kg_div_m2 = models.CharField(null=True, max_length=15)

    class Meta:
        abstract = True


### ПОМИДОРЫ


class TomatoTypeOfPlant(models.Model):
    name = models.CharField(null=False, max_length=19)  # детерминантный, супер-, ин-, полу-

    class Meta:
        db_table = "tomato_type_of_plant"


class GroundType(models.Model):
    name = models.CharField(null=False, max_length=8)  # закрытый открытый

    class Meta:
        db_table = "ground_type"


class TomatoSeeds(Product, SimpleSeeds):
    image = models.ImageField(blank=True, upload_to='product_img/TomatoSeeds', null=True)
    type_of_plant = models.ForeignKey(TomatoTypeOfPlant, on_delete=models.CASCADE)
    ground_growing_conditions = models.ForeignKey(GroundType, on_delete=models.CASCADE)

    class Meta:
        db_table = "tomato_seeds"


# VARIABLES
PRODUCT_TABLES = [TomatoSeeds]
STRING_TO_TABLE = {"TomatoSeeds": TomatoSeeds}
TABLE_TO_STRING = {}
for i, j in STRING_TO_TABLE.items():
    TABLE_TO_STRING[j] = i
