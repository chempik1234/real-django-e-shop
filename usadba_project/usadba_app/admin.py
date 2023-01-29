from django.contrib import admin
from .models import PRODUCT_TABLES, SeedsCategories, TomatoTypeOfPlant, RipeningPeriods, GroundType

# Register your models here.
for i in PRODUCT_TABLES + [SeedsCategories, TomatoTypeOfPlant, RipeningPeriods, GroundType]:
    admin.site.register(i)