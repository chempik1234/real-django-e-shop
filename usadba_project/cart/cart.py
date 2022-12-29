from decimal import Decimal
from django.conf import settings
from usadba_app.models import PRODUCT_TABLES, STRING_TO_TABLE

DIVIDER = "_DVD_"  # NEVER CHANGE THIS CONST!!!!!!!!!!!!


def get_product_key(product):
    return product._meta.db_table + DIVIDER + str(product.id)


def tomato_seeds_to_TomatoSeeds(string):
    res = string[0].upper()
    for i in range(1, len(string)):
        if string[i] == "_":
            continue
        if string[i - 1] == "_":
            res += string[i].upper()
        else:
            res += string[i]
    return res


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):  # tomato_seeds ?
        # на вход подаётся словарь {"table_DIV_id": {"product": <class>, "price": int, ...} }
        cart_product_tables_ids_undivided = self.cart.keys()
        cart_product_tables_ids = {}
        # заполняем словарь в виде {"table": [id, id, id......]}
        for undived_elem in cart_product_tables_ids_undivided:
            dived_elem = undived_elem.split(DIVIDER)
            if dived_elem[0] in cart_product_tables_ids.keys():
                cart_product_tables_ids[dived_elem[0]].append(int(dived_elem[1]))
            else:
                cart_product_tables_ids[dived_elem[0]] = [int(dived_elem[1])]
        # заполняем словарь {"table_DIV_id": <class inherited from Product>}
        keys_and_products = []
        for table_name, ids in cart_product_tables_ids.items():
            table = STRING_TO_TABLE[tomato_seeds_to_TomatoSeeds(table_name)]
            for found_product in table.objects.filter(id__in=ids):
                keys_and_products.append((table_name + DIVIDER + str(found_product.id), found_product))

        cart = self.cart.copy()
        for key, product in keys_and_products:
            cart[key]['product'] = product
            cart[key]['product_type'] = tomato_seeds_to_TomatoSeeds(product._meta.db_table)

        for item in cart.values():  # cart = {"table_DIV_id": {"product": <TomatoSeeds Row>} }
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']  # item = {"product": <TomatoSeeds Row>, "price": ...
            yield item

    def __len__(self):
        """
        Считаем сколько товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1):
        """
        Добавляем товар в корзину или обновляем его количество.
        """
        product_key = get_product_key(product)
        if product_key not in self.cart:
            self.cart[product_key] = {'quantity': 0,
                                      'price': str(product.price)}
        self.cart[product_key]['quantity'] = quantity
        self.save()

    def save(self):
        # сохраняем товар
        self.session.modified = True

    def remove(self, product):
        """
        Удаляем товар
        """
        product_key = get_product_key(product)
        if product_key in self.cart:
            del self.cart[product_key]
            self.save()

    def get_total_price(self):
        # получаем общую стоимость
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # очищаем корзину в сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def is_empty(self):
        if not self.cart:
            return True
        else:
            return False