"""frontul URL Configuration

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
    url(r'^home/', views.displayCells, name="displayCells"),
    url(r'^login/', views.login, name="login"),
    url(r'^signup/', views.signup, name="signup"),
    url(r'^catpost/(?P<catID>\d+)$', views.displayCatPosts, name="displayPosts"),
    url(r'^subcatpost/(?P<subCatID>\d+)$', views.displaySubCatPosts, name="displaySubCatPosts"),
    url(r'^create_post/', views.create_post, name="create_post"),
    url(r'^logout/', views.logoutUser, name="logoutUser"),
]
