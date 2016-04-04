"""uvalist URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),

    url(r'^api/v1/category$', views.list_category, name="list_category"),
    url(r'^api/v1/create_category$', views.create_category, name="create_category"),
    url(r'^api/v1/category/(?P<category_id>\d+)$', views.category, name="category"),

    url(r'^api/v1/subcategory$', views.list_subcategory, name="list_subcategory"),
    url(r'^api/v1/subcategory/(?P<subcategory_id>\d+)$', views.subcategory, name="subcategory"),

    url(r'^api/v1/student$', views.list_student, name="list_student"),
    url(r'^api/v1/create_student/$', views.create_student, name="create_student"),
    url(r'^api/v1/get_student/(?P<student_id>\d+)$', views.get_student, name="get_student"),




    url(r'^api/v1/get_category/(?P<cat_id>\d+)$', views.get_category, name="get_category"),
    url(r'^api/v1/student/(?P<student_id>\d+)$', views.student, name="student"),
    url(r'^api/v1/student/(?P<name>\w+)$', views.getStudentByUsername, name="getStudentByUsername"),
    url(r'^api/v1/studentByEmail/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', views.getStudentByEmail, name="getStudentByEmail"),



    url(r'^api/v1/post$', views.list_post, name="list_post"),
    url(r'^api/v1/post/(\d+)$', views.post, name="post"),
    url(r'^api/v1/create_post/$', views.create_post, name="create_post"),

    url(r'^api/v1/comment$', views.list_comment, name="list_comment"),
    url(r'^api/v1/comment/(?P<comment_id>\d+)$', views.comment, name="comment"),

    url(r'^api/v1/authenticator/$', views.authenticator, name="authenticator"),
    url(r'^api/v1/authenticator/(?P<user_id>\d+)$', views.authenticator, name="authenticator"),
    # url(r'^api/v1/get_user_by_authenticator/(?P<authenticator>\d+)$', views.get_user_by_authenticator, name="get_user_by_authenticator"),
    url(r'^api/v1/get_userid_auth/(?P<auth>\w+)$', views.get_userid_auth, name="get_userid_auth"),


]
