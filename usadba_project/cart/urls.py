from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views, yookassa

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<str:tableName>/<int:product_id>/',
         views.cart_add,
         name='cart_add'),
    path('remove/<str:tableName>/<int:product_id>/',
         views.cart_remove,
         name='cart_remove'),
    path('clear/',
         views.cart_clear,
         name='cart_clear'),
    path('order/',
         login_required(views.OrderView.as_view()),
         name='cart_fill_in_order'),
    path('order/online_pay/<int:order_id>',
         login_required(yookassa.YooPayment.as_view()),
         name='online_pay'),
    path('order/online_pay/<int:order_id>',
         login_required(yookassa.YooPayment.as_view()),
         name='online_pay'),
    path('order/order_success/<str:order_id>',
         login_required(views.order_success),
         name='order_success')
]