from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt 
import hmac
import os
# import settings
import datetime
from django.utils.timezone import utc

def index(request):
    return HttpResponse("Hello, world! Welcome to the very beginning of UVaList.")

def list_category(request):
    result = serializers.serialize('json', Category.objects.all())
    return HttpResponse(result, content_type='json')

def category(request, category_id):
    if request.method == "POST":
        title = request.POST.get('title', 'title did not work')
        category = Category.objects.create(title=title)
        category.save()
        curr_id = category.id
        result = serializers.serialize('json', Category.objects.filter(id=curr_id))
        return HttpResponse(result, content_type='json')
    result = serializers.serialize('json', Category.objects.filter(id=category_id))
    return HttpResponse(result, content_type='json')

def list_subcategory(request):
    result = serializers.serialize('json', Subcategory.objects.all())
    return HttpResponse(result, content_type='json')

def subcategory(request, subcategory_id):
    result = serializers.serialize('json', Subcategory.objects.filter(id=subcategory_id))
    return HttpResponse(result, content_type='json')

def list_student(request):
    result = serializers.serialize('json', Student.objects.all())
    return HttpResponse(result, content_type='json')

def student(request, student_id):
    if request.method == "POST":
        name = request.POST.get('name', 'name didnt work')
        gender = request.POST.get('gender', 'False')
        year = request.POST.get('year', '123')
        email = request.POST.get('email', 'email didnt work')
        password = request.POST.get('password', 'password didnt work')
        student = Student.objects.create(name=name, gender=gender, year=year, email=email, password=password)
        student.save()
        curr_id = student.id
        result = serializers.serialize('json', Student.objects.filter(id=curr_id))
        return HttpResponse(result, content_type='json')
    result = serializers.serialize('json', Student.objects.filter(id=student_id))
    return HttpResponse(result, content_type='json')

def list_post(request):
    result = serializers.serialize('json', Post.objects.all())
    return HttpResponse(result, content_type='json')

def post(request, post_id):
    result = serializers.serialize('json', Post.objects.filter(id=post_id))
    return HttpResponse(result, content_type='json')

def list_comment(request):
    result = serializers.serialize('json', Comment.objects.all())
    return HttpResponse(result, content_type='json')

def comment(request, comment_id):
    if request.method == "DELETE":
        Comment.objects.filter(id=comment_id).delete()
        return HttpResponse('')
    result = serializers.serialize('json', Comment.objects.filter(id=comment_id))
    return HttpResponse(result, content_type='json')

def authenticator(request, user_id, authenticator):
    #creating new one
    if request.method == "POST":
        user_id = user_id
        authenticator1 = hmac.new (key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256').hexdigest()
        date_created = datetime.datetime.now()
        result = serializers.serialize('json', Authenticator.objects.filter(authenticator=authenticator1))
        return HttpResponse(result, content_type='json')
    #getting existing one
    result = serializers.serialize('json', Authenticator.objects.filter(authenticator=authenticator))
    return HttpResponse(result, content_type='json')

