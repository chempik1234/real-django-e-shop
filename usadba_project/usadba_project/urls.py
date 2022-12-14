"""usadba_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path, include, re_path
from usadba_app.views import *
from git_pull.views import *
from usadba_project import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('usadba_app.urls')),
    path('', landing),
    path('github_update_pythonanywhere', github_update_pythonanywhere),
    re_path(r'^search/$', SearchList.as_view()),
    # path('search', search),
    path('categories', categories),
    path('profile', profile),
    path('register', register),
    path('accounts/login/', log_in),
    path('login', log_in),
    re_path(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('product/opinion/<str:pr_table>/<int:pr_id>', login_required(OpinionView.as_view(), login_url='/login')),
    path('product/buy/', product_buy),  # <str:product_table>/<int:id> L6rHDOlWhBiAW8H4iv1TT2Jy
    path('rate', leave_rate),
    path('product/<str:product_type>/<int:pr_id>', Product.as_view()),
    path('product/<str:product_type>', ProductListView.as_view()),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
