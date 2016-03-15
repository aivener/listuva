"""expul URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/maketable$', views.makeTable, name="makeTable"),
    url(r'^api/v1/postbycat/(?P<catID>\d+)$', views.getPostsByCategory, name="postsByCat"),
    url(r'^api/v1/postbysubcat/(?P<subcatID>\d+)$', views.getPostsBySubcategory, name="postsBySubcat"),
    url(r'^api/v1/getcatname/(?P<catID>\d+)$', views.getCatName, name="getCatName"),
    url(r'^api/v1/getsubcatname/(?P<subcatID>\d+)$', views.getSubcatName, name="getSubcatName"),
    url(r'^api/v1/catname/(?P<subcatID>\d+)$', views.getCatNameFromSubcat, name="getCatNameFromSubcat"),
    url(r'^api/v1/login$', views.login, name="login"),
    url(r'^api/v1/login_exp_api/username=(?P<username>\d+$)&password=(?P<password>\d+$)', views.login, name="login"),
]
]
