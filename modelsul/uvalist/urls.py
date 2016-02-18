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
    url(r'^api/v1/category/(?P<category_id>\d+)$', views.category, name="category"),

    url(r'^api/v1/subcategory$', views.list_subcategory, name="list_subcategory"),
    url(r'^api/v1/subcategory/(?P<subcategory_id>\d+)$', views.subcategory, name="subcategory"),

    url(r'^api/v1/student$', views.list_student, name="list_student"),
    url(r'^api/v1/student/(?P<student_id>\d+)$', views.student, name="student"),

    url(r'^api/v1/post$', views.list_post, name="list_post"),
    url(r'^api/v1/post/(?P<post_id>\d+)$', views.post, name="post"),

    url(r'^api/v1/comment$', views.list_comment, name="list_comment"),
    url(r'^api/v1/comment/(?P<comment_id>\d+)$', views.comment, name="comment"),

]