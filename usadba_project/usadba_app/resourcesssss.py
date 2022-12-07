from django.http.response import HttpResponseNotAllowed
from .models import PRODUCT_TABLES, TABLE_TO_STRING, Rates
from .views import get_rating


class BaseResource(object):

    __METHODS = {
        'GET': 'get',
        'POST': 'post',
    }

    def __init__(self, methods):
        self.methods = {}
        for i in methods:
            if i in self.__METHODS.keys():
                self.methods[i] = self.__METHODS[i]
        # here you look what allowed methods are in class init
        # and add it to self.methods

    def _process_body(self, request):
        request.data = None # here you will handle request and put json into variable

    def __call__(self, request, **kwargs):
        # here you look which method of view you must call

        if not request.method in self.methods:
            return HttpResponseNotAllowed(self.methods)

        attr = self.methods[request.method]
        func = getattr(self, attr, None)

        self._process_body(request)
        response = func(request, **kwargs)

        return response


class SearchResource(BaseResource):
    def get(self, request):
        text = request.GET.get("text")
        items = []
        if text:
            current_user = request.user
            for table in PRODUCT_TABLES:
                items_found_in_table = table.objects.filter(title__icontains=text)
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
        return items
