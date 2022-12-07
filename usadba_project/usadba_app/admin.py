from django.contrib import admin
from .models import PRODUCT_TABLES, SeedsCategories

# Register your models here.
for i in PRODUCT_TABLES + [SeedsCategories]:
    admin.site.register(i)