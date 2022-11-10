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
from django.urls import path
from usadba_app.views import *
from git_pull.views import *
from usadba_project import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', landing),
    path('github_update_pythonanywhere', github_update_pythonanywhere),
    path('search', search),
    path('categories', categories),
    path('profile', profile),
    path('register', register),
    path('login', log_in),
    path('logout', logout_),
    path('product/add_opinion/<str:pr_table>/<int:pr_id>', add_opinion),
    path('product/del_opinion/<str:pr_table>/<int:pr_id>', del_opinion),
    path('product/buy/<str:product_type>/<str:title>', product_buy),
    path('rate', leave_rate),
    path('product/<str:product_type>/<int:pr_id>', product),
    path('product/<str:product_type>', product_list),
    path('admin/', admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)