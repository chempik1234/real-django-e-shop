from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from usadba_app.models import STRING_TO_TABLE
from .cart import Cart
from .forms import CartAddProductForm
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
    return render(request, 'cart/detail.html', context=CONTEXT)