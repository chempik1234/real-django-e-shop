from django.db import models
from random import randint
from django.urls import reverse
import os
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


def check_float(string):
    if string.isdigit():
        return True
    not_digit_symbs, not_digit_symbol = 0, ''
    for i in string:
        if not i.isdigit():
            not_digit_symbs += 1; not_digit_symbol = i
    if not_digit_symbs > 1:
        return False
    if not_digit_symbol == '.':
        if string.index(not_digit_symbol) > 0:
            return True
        return False


def create_random_string():
    s, r = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890', ''
    for i in range(30):
        if i == 15:
            r += '-'
            continue
        r += s[randint(0, len(s) - 1)]
    return r


# Create your models here.


# class Cart(models.Model):
#     user_id = models.IntegerField(unique=True)
#
#
# class CartAndProduct(models.Model):
#     order_id = models.IntegerField


class Opinion(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(null=True,max_length=1200, verbose_name="Текст")
    image = models.ImageField(null=True, blank=True, upload_to='opinion', verbose_name="Изображение")
    pr_table = models.CharField(null=True,max_length=255)  # tomato_seeds
    pr_id = models.IntegerField(null=True)
    proven = models.BooleanField(null=False, default=False, verbose_name="Доказан")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        db_table = "opinion"


class Product(models.Model):
    title = models.CharField(null=False, max_length=255, default="DEFAULT NAME12345", verbose_name="Название")
    image = None #models.ImageField(upload_to=os.path.join(os.curdir, '../static/img/product_img'))
    description = models.CharField(null=True, max_length=500, verbose_name="Описание")
    price = models.IntegerField(null=False, default=1, validators=[MinValueValidator(1)], verbose_name="Цена")
    company = models.CharField(null=True, max_length=50, verbose_name="Компания")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        abstract = True

    def __str__(self):
        return self.title


class Rates(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(null=False, default=1, validators=[MaxValueValidator(5), MinValueValidator(1)],
                               verbose_name="Оценка")
    pr_table = models.CharField(null=True,max_length=255)  # tomato_seeds
    pr_id = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        db_table = "rates"


class Orders(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(_("date joined"), default=timezone.now)
    is_deliver = models.BooleanField()
    is_cash = models.BooleanField()
    has_been_paid = models.BooleanField(default=False)
    where_to_deliver_coords_comma = models.CharField(null=True, max_length=100)
    yookassa_id = models.CharField(null=True, max_length=36 + 4)
    unique_id = models.CharField(unique=True, max_length=30, default=create_random_string)

    def clean(self):
        if self.where_to_deliver_coords_comma:
            if len(self.where_to_deliver_coords_comma) >= 3 and ',' in self.where_to_deliver_coords_comma and ' ' not in self.where_to_deliver_coords_comma and \
                    check_float(self.where_to_deliver_coords_comma[: self.where_to_deliver_coords_comma.index(',')]) and \
                    check_float(self.where_to_deliver_coords_comma[self.where_to_deliver_coords_comma.index(',') + 1:]):
                pass
            else:
                raise ValidationError("Неправильный формат координат доставки, введённые данные:" +
                                      str(self.where_to_deliver_coords_comma))
        elif self.is_deliver == True and (not self.where_to_deliver_coords_comma or
                self.where_to_deliver_coords_comma is None):
            raise ValidationError("Если выбрана доставка, то надо указать место")
        elif self.is_deliver == True and self.is_cash == True:
            raise ValidationError("Если выбрана доставка, то нельзя выбрать оплату наличными")
        super().clean()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        db_table = "orders"


class OrderToProduct(models.Model):
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.IntegerField(validators=[MinValueValidator(1)])
    product_db_table = models.CharField(max_length=30)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        db_table = "order_to_product"


### СЕМЕНА
class SeedsCategories(models.Model):
    name = models.CharField(null=False, max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Категория семян (F1, F2...)"
        verbose_name_plural = "Категории семян (F1, F2...)"
        db_table = "seed_categories"

    def __str__(self):
        return self.name


class RipeningPeriods(models.Model):
    name = models.CharField(null=False, max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Период созревания (поздний, ..., ранний)"
        verbose_name_plural = "Периоды созревания (поздний, ..., ранний)"
        db_table = "ripening_periods"

    def __str__(self):
        return self.name


class GroundType(models.Model):
    name = models.CharField(null=False, max_length=8, verbose_name="Название")  # закрытый открытый

    class Meta:
        verbose_name = "Тип грунта (открытый/закрытый)"
        verbose_name_plural = "Типы грунта (открытый/закрытый)"
        db_table = "ground_type"

    def __str__(self):
        return self.name


class SimpleSeeds(models.Model):
    category = models.ForeignKey(SeedsCategories, on_delete=models.CASCADE, default=1, verbose_name="Категория")
    ripening_period = models.ForeignKey(RipeningPeriods, on_delete=models.CASCADE, default=1,
                                        verbose_name="Период созревания")
    ripe_color = models.CharField(null=True, max_length=30, verbose_name="Цвет плода")
    ripe_form = models.CharField(null=True, max_length=50, verbose_name="Форма плода")
    ripe_weight_grams = models.IntegerField(null=True, verbose_name="Вес плода (граммы)")
    yield_kg_div_m2 = models.CharField(null=True, max_length=15, verbose_name="Урожайность кг/м2")
    ground_growing_conditions = models.ForeignKey(GroundType, on_delete=models.CASCADE, verbose_name="Тип грунта")

    class Meta:
        abstract = True


### ПОМИДОРЫ


class TomatoTypeOfPlant(models.Model):
    name = models.CharField(null=False, max_length=19, verbose_name="Название")  # детерминантный, супер-, ин-, полу-

    class Meta:
        verbose_name = "Тип растения (ин-, полу-, супер- детерминантный)"
        verbose_name_plural = "Типы растения (ин-, полу-, супер- детерминантный)"
        db_table = "tomato_type_of_plant"

    def __str__(self):
        return self.name


class TomatoSeeds(Product, SimpleSeeds):
    image = models.ImageField(blank=True, upload_to='product_img/TomatoSeeds', null=True, verbose_name="Изображение")
    type_of_plant = models.ForeignKey(TomatoTypeOfPlant, on_delete=models.CASCADE, verbose_name="Тип растения")

    class Meta:
        verbose_name = "Упаковка семян помидоров"
        verbose_name_plural = "Семена помидоров"
        db_table = "tomato_seeds"


### ОГУРЦЫ
class CucumberSeeds(Product, SimpleSeeds):
    image = models.ImageField(blank=True, upload_to='product_img/CucumberSeeds', null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Упаковка семян огурцов"
        verbose_name_plural = "Семена огурцов"
        db_table = "cucumber_seeds"


# VARIABLES
PRODUCT_TABLES = [TomatoSeeds, CucumberSeeds]
STRING_TO_TABLE = {"TomatoSeeds": TomatoSeeds,
                   "CucumberSeeds": CucumberSeeds}
TABLE_TO_STRING = {}
for i, j in STRING_TO_TABLE.items():
    TABLE_TO_STRING[j] = i
STRING_TO_NAME_AND_TABLE = {i: (j._meta.verbose_name_plural, j) for i, j in STRING_TO_TABLE.items()}