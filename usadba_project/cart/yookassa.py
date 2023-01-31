from yookassa import Payment, Configuration
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import View
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from .cart import Cart, DIVIDER
from usadba_app.models import Orders, OrderToProduct, STRING_TO_TABLE
from .forms import CartAddProductForm, OrderFillForm
from django.contrib import messages
SEED_CATEGORIES = {'Помидоры': 'Tomato',
                   'Огурцы': 'Cucumber',
                   'Морковь': 'Carrot',
                   'Капуста': 'Cabbage'}
DEFAULT_CONTEXT = {
    # "styles": STYLE_FILES,
    "seed_categories": SEED_CATEGORIES,
    "main_title": "Корзина",
    "title": "Корзина",
    # "general_images_dirs": GENERAL_IMAGES_DIRS
}


def remove_underlines(string):
    res = string[0].upper()
    for i in range(1, len(string)):
        if string[i] == "_":
            continue
        if string[i - 1] == "_":
            res += string[i].upper()
        else:
            res += string[i]
    return res


def add_underlines(string):
    res = string[0].lower()
    for i in range(1, len(string)):
        if string[i].isupper():
            res += "_"
        res += string[i].lower()
    return res


class YooPayment(View):
    def get(self, request, order_id):
        Configuration.account_id = '980187'
        Configuration.secret_key = 'test_4Kh13LvH8qXJrbsDtEM9O8rDPb1EVv4effgxYteZA2g'

        dat_order = get_object_or_404(Orders, id=order_id)
        products = OrderToProduct.objects.filter(order_id=order_id)
        price = sum([STRING_TO_TABLE[remove_underlines(i.product_db_table)].objects.get(id=i.product_id).price *
                     i.quantity for i in products])
        print(price)

        payment = Payment.create({
            "amount": {
                "value": str(price),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://imfighter160.pythonanywhere.com/cart/order/order_success/" + str(order_id)
            },
            "capture": True,
            "description": "Тестовый заказ"
        }, uuid.uuid4())
          # "payment_id": "215d8da0-000f-50be-b000-0003308c89be"
        dat_order.yookassa_id = payment.id
        dat_order.save()
        return HttpResponseRedirect(payment.confirmation.confirmation_url)
