from django.contrib import admin

from .models import Student, Category, Subcategory, Post, Comment

admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Post)
admin.site.register(Comment)
