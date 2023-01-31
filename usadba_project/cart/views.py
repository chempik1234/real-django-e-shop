from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from usadba_app.models import STRING_TO_TABLE
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from .cart import Cart, DIVIDER
from usadba_app.models import Orders, OrderToProduct
from .forms import CartAddProductForm, OrderFillForm
from django.contrib import messages
from yookassa import Payment, Configuration
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


@require_POST
def cart_add(request, tableName, product_id):
    cart = Cart(request)
    tableName = remove_underlines(tableName)
    Model = STRING_TO_TABLE[tableName]
    product = get_object_or_404(Model, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'])
    return redirect('cart:cart_detail')


def cart_remove(request, tableName, product_id):
    cart = Cart(request)
    tableName = remove_underlines(tableName)
    Model = STRING_TO_TABLE[tableName]
    product = get_object_or_404(Model, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    CONTEXT = DEFAULT_CONTEXT.copy()
    CONTEXT["cart"] = cart
    CONTEXT["title"] = str(cart.get_total_price()) + "р (корзина)"
    CONTEXT["main_title"] = "Корзина"
    return render(request, 'cart/detail.html', context=CONTEXT)


class OrderView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cart/order.html'

    def get(self, request):
        cart = Cart(request)
        if cart.is_empty():
            messages.error(request, "Корзина пуста")
            return HttpResponseRedirect('/')
        # for item in cart:
        #     item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
        #                                 'update': True})
        form = OrderFillForm()
        CONTEXT = DEFAULT_CONTEXT.copy()
        CONTEXT["form"] = form
        CONTEXT["price"] = cart.get_total_price()
        CONTEXT["title"] = str(cart.get_total_price()) + "р (заказ)"
        CONTEXT["main_title"] = "Оформление заказа"
        return Response(CONTEXT)

    def post(self, request):
        post = OrderFillForm(request.POST)
        if post.is_valid():
            is_cash = post.cleaned_data.get('cash_or_card')
            print(post.cleaned_data)
            is_deliver = post.cleaned_data.get('deliver_or_pickup')
            coords = post.cleaned_data.get('location')
            order = Orders()
            order.user_id = request.user
            order.is_deliver = is_deliver
            if is_cash == "False":
                is_cash = False
            else:
                is_cash = True
            order.is_cash = is_cash
            if coords:
                order.where_to_deliver_coords_comma = coords
            try:
                order.clean()
                order.save()
                cart = Cart(request)
                if cart.is_empty():
                    messages.error(request, "Корзина пуста")
                    return HttpResponseRedirect('/')
                for i in cart:
                    pr_type, pr_id, quantity = i["product_type"], i['product'].id, i['quantity']
                    otp = OrderToProduct()
                    otp.order_id = order
                    otp.product_id = pr_id
                    otp.product_db_table = add_underlines(pr_type)
                    otp.quantity = quantity
                    otp.save()
                cart.clear()
                if not is_cash:
                    return HttpResponseRedirect('online_pay/' + str(order.id))
                return HttpResponseRedirect("order_success/" + str(order.id))
            except ValidationError as err:
                # CONTEXT = DEFAULT_CONTEXT.copy()
                messages.error(request, err.message)
        return self.get(request)


def order_success(request, order_id):
    CONTEXT = DEFAULT_CONTEXT.copy()
    CONTEXT["main_title"] = "Завершение"
    CONTEXT["title"] = "Завершение оформления заказа"
    order = Orders.objects.filter(id=order_id)
    if order.exists():
        order = order.first()
        if Payment.find_one(order.yookassa_id).status == "succeeded":
            order.has_been_paid = True
            order.save()
        CONTEXT["order"] = {"products": [], "price": 0, "datetime": order.date_created,
                            "is_deliver": order.is_deliver, "has_been_paid": order.has_been_paid}
        for product in OrderToProduct.objects.filter(order_id=order):
            product_model_object = get_object_or_404(STRING_TO_TABLE[remove_underlines(product.product_db_table)],
                                                     id=product.product_id)
            CONTEXT["order"]["products"].append({"product": product_model_object,
                                                 "quantity": product.quantity})
            CONTEXT["order"]["price"] += product_model_object.price
    else:
        CONTEXT["order"] = None

    CONTEXT["id"] = order_id
    return render(request, 'cart/order_success.html', context=CONTEXT)


Configuration.account_id = '980187'
Configuration.secret_key = 'test_4Kh13LvH8qXJrbsDtEM9O8rDPb1EVv4effgxYteZA2g'
