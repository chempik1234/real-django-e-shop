from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.views.decorators.http import require_POST
from django.core.files import File
import urllib.request
from .models import *
from .forms import *
from django.db.models import Sum
import os, requests, datetime
# from os import listdir
# from os.path import isfile, join, basename
from random import randint
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader_tags import register
from django.contrib import messages
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
SEED_CATEGORIES = {'Помидоры': 'Tomato',
                   'Огурцы': 'Cucumber',
                   'Морковь': 'Carrot',
                   'Капуста': 'Cabbage'}
# URL_STYLE_PATH = os.path.join('../static', 'css')
# STYLE_FILES = [basename(i) for i in listdir(URL_STYLE_PATH) if isfile(join(URL_STYLE_PATH, i))]
# STATIC_IMG_GENERAL = '/static/img/general/'
# GENERAL_IMAGES_DIRS = {'bucket': STATIC_IMG_GENERAL + 'bucket.png',
#                        'star': STATIC_IMG_GENERAL + 'star.png',
#                        'star_gray': STATIC_IMG_GENERAL + 'star_gray.png',
#                        'map_icon': STATIC_IMG_GENERAL + 'map_icon.png',
#                        'seeds': STATIC_IMG_GENERAL + 'seeds.png',
#                        'percent': STATIC_IMG_GENERAL + 'percent.png'}
DEFAULT_CONTEXT = {
    # "styles": STYLE_FILES,
    "seed_categories": SEED_CATEGORIES,
    # "general_images_dirs": GENERAL_IMAGES_DIRS
}


def x_or_y_if_a(a, x, y):
    if a is None:
        return None
    elif not a:
        return x
    else:
        return y


def get_rating(model_, id):
    rates = Rates.objects.filter(pr_table=model_._meta.db_table,pr_id=id)
    res, c = rates.aggregate(Sum('rate')), 0
    if res["rate__sum"]:
        c = res["rate__sum"]
    else:
        c = 0
    return round(c / max(len(rates), 1), 1)


@register.filter(name='range')
def filter_range(start, end):
    return range(int(start), int(end))


# Views
def search(request):
    q = request.GET.get('q', '')
    data_context = DEFAULT_CONTEXT.copy()
    data_context["main_title"] = "Результаты поиска: " + q
    data_context["title"] = "Результаты поиска"
    items = []
    current_user = request.user
    for table in PRODUCT_TABLES:
        items_found_in_table = table.objects.filter(title__icontains=q)
        for item in items_found_in_table:
            your_rate = Rates.objects.filter(user_id=current_user, pr_table=item._meta.db_table, pr_id=item.id)
            if your_rate.exists():
                your_rate = your_rate.first().rate
            else:
                your_rate = 0
            items.append({'title': item.title,
                          'price': item.price,
                          'rating': get_rating(table, item.id),
                          'your_rate': your_rate,
                          'id': item.id,
                          'product_type': TABLE_TO_STRING[table]})
    data_context["dictionary"] = items
    data_context["seed_categories"] = SEED_CATEGORIES
    return render(request, 'usadba_app/list.html', context=data_context)


def landing(request):
    data = DEFAULT_CONTEXT.copy()
    data["main_title"] = "Главная"
    return render(request, 'usadba_app/landing.html', context=data)


def categories(request):
    index_categories = {"Семена": ("seeds", "TomatoSeeds")}
    data = DEFAULT_CONTEXT.copy()
    data["main_title"] = "Категории"
    data["categories"] = index_categories
    return render(request, 'usadba_app/categories.html', context=data)


def product_list(request, product_type):
    d = []
    types = {'TomatoSeeds': ('Семена помидоров', TomatoSeeds)}
    table = types[product_type][1]
    current_user = request.user
    for item in table.objects.all():
        your_rate = 0
        if current_user.is_authenticated:
            your_rate = Rates.objects.filter(user_id=current_user,pr_table=item._meta.db_table,pr_id=item.id)
            if your_rate.exists():
                your_rate = your_rate.first().rate
        d.append({'title': item.title,
                  'price': item.price,
                  'rating': get_rating(table, item.id),
                  'your_rate': your_rate,
                  'id': item.id,
                  'product_type': product_type,
                  'image_url': item.image.url})
    data_context = DEFAULT_CONTEXT.copy()
    data_context["title"] = types[product_type][0]
    data_context["main_title"] = types[product_type][0]
    data_context["dictionary"] = d
    data_context["seed_categories"] = SEED_CATEGORIES
    data_context["main_title"] = types[product_type][0]
    return render(request, 'usadba_app/list.html', context=data_context)


def product(request, product_type, pr_id):
    tables = {'TomatoSeeds': TomatoSeeds}
    item_model = tables[product_type]
    item = item_model.objects.get(id=pr_id)
    title = item.title
    d = {}
    if "Seeds" in product_type:
        d["Категория"] = item.category.name
        d["Период созревания"] = item.ripening_period.name
        d["Цвет плода"] = item.ripe_color
        d["Форма плода"] = item.ripe_form
        d["Вес плода в граммах"] = item.ripe_weight_grams
        d["Урожайность на квадратный метр"] = str(item.yield_kg_div_m2) + " кг"
    if "Tomato" in product_type:
        d["Тип растения"] = item.type_of_plant.name
        d["Условия выращивания"] = item.ground_growing_conditions.name + ' грунт'
    opinions_db = Opinion.objects.filter(pr_table=product_type, pr_id=item.id)
    opinions = []
    for i in opinions_db:
        some_user = i.user_id
        some_rate = Rates.objects.filter(user_id=some_user,pr_table=item_model._meta.db_table,pr_id=item.id)
        if some_rate.exists():
            some_rate = some_rate.first().rate
        else:
            some_rate = 0
        opinions.append([some_user.username, i.text, i.image, some_rate])
    current_user = request.user
    if not opinions:
        opinions = None
    your_op, your_rate = False, 0
    if current_user.is_authenticated:
        if Opinion.objects.filter(pr_table=product_type, pr_id=item.id, user_id=current_user).exists():
            your_op = True
        your_rate = Rates.objects.filter(user_id=current_user,pr_table=item._meta.db_table,pr_id=item.id)
        if your_rate.exists():
            your_rate = your_rate.first().rate
    data_context = DEFAULT_CONTEXT.copy()
    data_context["item"] = d.items()
    data_context["product_type"] = product_type
    data_context["price"] = item.price
    data_context["description"] = item.description
    data_context["rate"] = get_rating(item_model, item.id)
    data_context["img_dir"] = '/product_img/' + product_type
    data_context["title"] = title
    data_context["id"] = item.id
    data_context["opinions"] = opinions
    data_context["your_rate"] = your_rate
    data_context["img_url"] = item.image.url
    data_context["have_opinion"] = your_op
    # data_context["rating_bar_form"] = RatingBar
    return render(request, 'usadba_app/product.html', context=data_context)


@require_POST
@login_required(login_url='/login')
def leave_rate(request):
    rate, product_type, pr_id = request.POST.get('rate'),\
                                request.POST.get('product_type'),\
                                request.POST.get('id')
    # if form.is_valid():
    #     print(request.POST)
    #     rate, product_type, pr_id = form.cleaned_data.get('rate'),\
    #                                 form.cleaned_data.get('product_type'),\
    #                                 form.cleaned_data.get('id')
    #     print(rate, product_type, pr_id)
    # else:
    #     return HttpResponseBadRequest("Rating bar form is not valid (this is impossible)")
    table = STRING_TO_TABLE[product_type]
    item = table.objects.get(id=pr_id)
    if item:
        title = item.title
        current_user = request.user
        existing_rate = Rates.objects.filter(pr_id=pr_id,pr_table=table._meta.db_table,user_id=current_user)
        if not existing_rate.exists():
            rate_obj = Rates(user_id=current_user,rate=rate,pr_table=table._meta.db_table,pr_id=pr_id)
            rate_obj.save()
        else:
            rate_obj = existing_rate.first()
            rate_obj.rate = rate
            rate_obj.save(update_fields=['rate'])
        return HttpResponseRedirect(f'/product/{product_type}/{pr_id}')
    else:
        return HttpResponseNotFound("")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def download_file(request, name):
#     if request.method == 'POST':
#         title = request.POST['title']
#         upload1 = request.FILES['upload']
#         object = Upload.objects.create(title=title, upload=upload1)
#         object.save()
#     return HttpResponseRedirect()


@login_required(login_url='/login')
def add_opinion(request, pr_table, pr_id):
    current_user = request.user
    described_items = STRING_TO_TABLE[pr_table].objects.filter(id=pr_id)
    if not described_items.exists():
        return HttpResponseNotFound("")
    described_item = described_items.first()
    pr_title = described_item.title
    if Opinion.objects.filter(pr_table=pr_table,pr_id=pr_id,user_id=current_user.id).exists():
        messages.error(request, "Вы уже оставили отзыв.")
        return product(request, pr_table, pr_title)
    if request.method == 'POST':
        post = OpinionForm(request.POST, request.FILES)
        if post.is_valid():
            text, file = post.cleaned_data.get('text'), post.cleaned_data.get('file')
            op = Opinion()
            op.user_id = current_user
            op.text = text
            op.pr_table = pr_table
            op.pr_id = pr_id
            if file:
                op.image = file
            op.save()
            print('saved')
        else:
            print(post.cleaned_data)
        return HttpResponseRedirect(f'/product/{pr_table}/{pr_id}')
    form_ = OpinionForm()
    data_context = DEFAULT_CONTEXT.copy()
    data_context["item_title"] = pr_title
    data_context["main_title"] = "Оставить отзыв на " + pr_title
    data_context["title"] = data_context["main_title"]
    data_context["product_type"] = pr_table
    data_context["form"] = form_
    data_context["img_url"] = described_item.image.url
    return render(request, 'usadba_app/opinion.html', context=data_context)


@login_required(login_url='/login')
def del_opinion(request, pr_table, pr_id):
    if request.method == 'POST':
        opinion = Opinion.objects.filter(pr_table=pr_table,pr_id=pr_id,user_id=request.user)
        if opinion.exists():
            opinion.delete()
            return HttpResponseRedirect('/product/{0}/{1}'.format(pr_table, pr_id))
        else:
            return HttpResponse('YOUR (!) opinion does not exist', status=400)
    else:
        return HttpResponse('required_post', status=400)


@login_required(login_url='/login')
def profile(request):
    data_context = DEFAULT_CONTEXT.copy()
    data_context["title"] = "Профиль"
    data_context["main_title"] = "Профиль"
    current_user = request.user
    user_info = [("Имя", current_user.first_name),
                 ("Фамилия", current_user.last_name),
                 ("Логин / Почта", current_user.email),
                 ("Дата регистрации", current_user.date_joined)]
    data_context["user_info"] = user_info
    data_context["username"] = current_user.username
    return render(request, 'usadba_app/profile.html', context=data_context)


@login_required(login_url='/login')
def product_buy(request, product_type, title):
    # tables = {'cpu': CPU, 'gpu': GPU, 'motherboard': Motherboard}
    # item = tables[product_type].objects.get(title=title)
    # price = item.price
    # json_ = {
    #     "caption": "Покупка товара",
    #     "description": "Название: " + title,
    #     "meta": title + product_type + str(randint(100000, 999999)),
    #     "autoclear": True,
    #     "items": [
    #         {
    #             "name": title,
    #             "price": str(price),
    #             "nds": "nds_10",
    #             "currency": "RUB",
    #             "amount": 1,
    #             "image": {
    #                 "url": os.path.join('\static', f'img/{product_type}/{title}.jpg')
    #           }
    #         }
    #       ],
    #     "mode": "test",
    #     "return_url": "/product/" + product_type
    #     }
    # requests.post('https://pay-sdk.yandex.net/v1', json=json_)
    return index(request)


def register(request):
    if request.method == 'POST':
        post = DBLoginForm(request.POST)
        if post.is_valid():
            post.save()
            #post.clean()
            #username = post.cleaned_data.get('username')
            #surname = post.cleaned_data.get('surname')
            #name = post.cleaned_data.get('name')
            #email = post.cleaned_data.get('email')
            #hashed_password = post.cleaned_data.get('password')
            #user = User()
            #user.username = username
            #user.last_name = surname
            #user.first_name = name
            #user.email = email
            #user.date_joined = datetime.datetime.now()
            #user.last_login = user.date_joined
            #user.password = hashed_password
            #user.save()
            return HttpResponseRedirect('/')
        else:
            form = post
    else:
        form = DBLoginForm()
    data_context = DEFAULT_CONTEXT.copy()
    data_context["title"] = "Регистрация"
    data_context["main_title"] = "Регистрация"
    data_context["form"] = form
    return render(request, 'usadba_app/sign_in.html', context=data_context)


def log_in(request):
    form = SignInForm()
    if request.method == 'POST':
        post = SignInForm(request.POST)
        if post.is_valid():
            post.clean()
            email = post.cleaned_data.get('email')
            password = post.cleaned_data.get('password')
            user = User.objects.get(email=email,password=password)# authenticate(request, email=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/")
        form = post
    data_context = DEFAULT_CONTEXT.copy()
    data_context["title"] = "Авторизация"
    data_context["main_title"] = "Авторизация"
    data_context["form"] = form
    return render(request, 'usadba_app/login.html', context=data_context)


@login_required(login_url='/login')
def logout_(request):
    logout(request)