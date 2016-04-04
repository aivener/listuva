from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import hmac
import os
from django.core import serializers
from django.conf import settings
import datetime
from django.utils.timezone import utc
from django.contrib.auth import hashers
from django import db
from django.forms.models import model_to_dict

def index(request):
    return HttpResponse("Hello, world! Welcome to the very beginning of UVaList.")


#List Methods
def list_category(request):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        result = serializers.serialize('json', Category.objects.all())
        return HttpResponse(result, content_type='json')
    except Category.DoesNotExist:
        return _error_response(request, "category not found")

def list_subcategory(request):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        result = serializers.serialize('json', Subcategory.objects.all())
        return HttpResponse(result, content_type='json')
    except Subcategory.DoesNotExist:
        return _error_response(request, "subcategory not found")

def subcategory(request, subcategory_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        result = serializers.serialize('json', Subcategory.objects.filter(id=subcategory_id))
        return HttpResponse(result, content_type='json')
    except Subcategory.DoesNotExist:
        return _error_response(request, "subcategory not found")

def list_student(request):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        result = serializers.serialize('json', Student.objects.all())
        return HttpResponse(result, content_type='json')
    except Student.DoesNotExist:
        return _error_response(request, "students not found")

def getStudentByUsername(request, name):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        s = Student.objects.filter(name=name)
        result = serializers.serialize('json', Student.objects.filter(name=name))
        return HttpResponse(result, content_type='json')

    except Student.DoesNotExist:
        return _error_response(request, "students not found")

def getStudentByEmail(request, email):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        s = Student.objects.filter(email=email)
        result = serializers.serialize('json', Student.objects.filter(email=email))
        return HttpResponse(result, content_type='json')

    except Student.DoesNotExist:
        return _error_response(request, "students not found")

def list_post(request):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        result = serializers.serialize('json', Post.objects.all())
        return HttpResponse(result, content_type='json')
    except Post.DoesNotExist:
        return _error_response(request, "post not found")

def post(request, post_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        result= model_to_dict(Post.objects.get(pk=post_id))
        return JsonResponse(result, content_type='json')
    except Post.DoesNotExist:
        return _error_response(request, "post not found")


def create_post(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'title' not in request.POST:
        return _error_response(request, request.POST)
    student = Student(pk=request.POST['user_id'])
    category = Category(pk=request.POST['category'])
    subcategory = Subcategory(pk=request.POST['subcategory'])

    p = Post(student = student,
        title = request.POST['title'],
        summary = request.POST['summary'],
        dateTimePosted = datetime.datetime.now(),
        price = request.POST['price'],
        active = True,
        category = category,
        subcategory =subcategory)
    p.save()
    post = model_to_dict(Post.objects.get(pk=p.pk))
    return JsonResponse(post)

def list_comment(request):
    result = serializers.serialize('json', Comment.objects.all())
    return HttpResponse(result, content_type='json')

#End List Methods

def comment(request, comment_id):
    if request.method == "DELETE":
        Comment.objects.filter(id=comment_id).delete()
        return HttpResponse('')
    result = serializers.serialize('json', Comment.objects.filter(id=comment_id))
    return HttpResponse(result, content_type='json')

def authenticator(request):
    #creating new one
    #u_id = user_id
    if request.method == "POST":
        u_id = request.POST.get('pk')
        #check if there already is an authenticator object for the user, if there is return that
        if(Authenticator.objects.filter(user_id_id=u_id).exists()):
            result = serializers.serialize('json', Authenticator.objects.filter(user_id_id=u_id))
            return HttpResponse(result)

        #if no authenticator object for this user, create a new one and return it
        authenticator1 = hmac.new (key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256').hexdigest()
        date_created = datetime.datetime.now()
        auth = Authenticator.objects.create(user_id_id=u_id, authenticator=authenticator1, date_created=date_created)
        auth.save()
        result = serializers.serialize('json', Authenticator.objects.filter(user_id_id=u_id))
        return HttpResponse(result, content_type='json')

    #getting existing one
    authenticator1 = hmac.new (key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256').hexdigest()
    result = serializers.serialize('json', Authenticator.objects.filter(user_id_id=u_id))
    return HttpResponse(result, content_type='json')

def create_student(request):
    #should add try catch statements
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'name' not in request.POST or 'gender' not in request.POST or 'year' not in request.POST or 'password' not in request.POST or 'email' not in request.POST:
        return _error_response(request, "missing required fields")

    s = Student(name = request.POST['name'],
                email = request.POST['email'],
                gender = request.POST['gender'],
                year = request.POST['year'],
                password=hashers.make_password(str.strip(request.POST['password'])),
                )
    try:
        s.save()
        result = serializers.serialize('json', Student.objects.filter(name=request.POST['name']))

        return HttpResponse(result, content_type='json')

    # except db.Error:
    except db.Error:
        return _error_response(request, "db error")
    return _success_response(request, {'user_id': s.pk})


def get_student(request, student_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        s = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return _error_response(request, "user not found")

    return _success_response(request, {'name': s.username,
                                       'gender': s.gender,
                                       'year': s.year,
                                       'password': s.password,
                                       'email': s.email
                                       })

#need to remove this method
def student(request, student_id):
    if request.method == "POST":
        name = request.POST.get('name', 'name didnt work')
        gender = request.POST.get('gender', 'default')
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

def create_category(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'title' not in request.POST:
        return _error_response(request, request.POST)

    s = Category(title = request.POST['title'])

    try:
        s.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'cat_id': s.pk})

def get_category(request, cat_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        s = Category.objects.get(pk=cat_id)
    except Category.DoesNotExist:
        return _error_response(request, "category not found")

    return _success_response(request, {'title': s.title })


def create_sucategory(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'title' not in request.POST or 'category' not in request.POST:
        return _error_response(request, "missing required fields")

    s = Subcategory(title = request.POST['title'], category = request.POST['category'])

    try:
        s.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'subcat_id': s.pk})

def get_sub_category(request, subcat_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        s = Subcategory.objects.get(pk=subcat_id)
    except models.Category.DoesNotExist:
        return _error_response(request, "category not found")

    return _success_response(request, {'title': s.title, 'category': s.category })

def get_userid_auth(request, auth): #get user id given auth code
    if request.method != 'GET':
        return _error_response(request, "must make GET request")
    try:
        auth = Authenticator.objects.get(pk=auth)
        student = auth.user_id
        user_id = student.pk
    except models.Authenticator.DoesNotExist:
        return _error_response(request, "category not found")
    return _success_response(request, {'user_id': user_id})

#need to remove this method
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


def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})
