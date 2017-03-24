"""lucky_express URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r"^blog/", include("blog.urls"))
"""
from django.conf.urls import url, include

from backpage.admin import mlssz_admin
from backpage import views
from backpage import apps

from django.contrib.auth.models import User

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r"^lessee/(?P<pk>[0-9]+)/pictures/$", views.lessee_pictures),
    url(r"^admin/", mlssz_admin.urls),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^rent/(?P<pk>[0-9]+)/near_lessees/$", views.NearLesseesList.as_view()),
    url(r"^datas/(?P<utype>[0-9])/$", views.DevDataList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
