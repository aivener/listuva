from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import hmac
import os
from django.conf import settings
import datetime
from django.utils.timezone import utc
from django.contrib.auth import hashers

def index(request):
    return HttpResponse("Hello, world! Welcome to the very beginning of UVaList.")


#List Methods
def list_category(request):
    result = serializers.serialize('json', Category.objects.all())
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

def studentByUsername(request, name):
    result = serializers.serialize('json', Student.objects.filter(name=name))
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
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'name' not in request.POST or 'gender' not in request.POST or 'year' not in request.POST or 'password' not in request.POST or 'email' not in request.POST:
        return _error_response(request, "missing required fields")

    s = models.Student(name = request.POST['name'],
                       gender = request.POST['gender'],
                       year = request.POST['year'],
                       password=hashers.make_password(request.POST['password']),
                       )

    try:
        s.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'user_id': s.pk})

def get_student(request, user_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        s = models.Student.objects.get(pk=user_id)
    except models.Student.DoesNotExist:
        return _error_response(request, "user not found")

    return _success_response(request, {'name': s.username,
                                       'gender': s.gender,
                                       'year': s.year,
                                       'password': s.password,
                                       'email': s.email
                                       })

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

def create_category(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'title' not in request.POST:
        return _error_response(request, "missing required fields")

    s = models.Category(name = request.POST['title'])

    try:
        s.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'cat_id': s.pk})

def get_category(request, cat_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        s = models.Category.objects.get(pk=cat_id)
    except models.Category.DoesNotExist:
        return _error_response(request, "category not found")

    return _success_response(request, {'title': s.title })


def create_sucategory(request):
    if request.method != 'POST':
        return _error_response(request, "must make POST request")
    if 'title' not in request.POST or 'category' not in request.POST:
        return _error_response(request, "missing required fields")

    s = models.Subcategory(name = request.POST['title'], category = request.POST['category'])

    try:
        s.save()
    except db.Error:
        return _error_response(request, "db error")

    return _success_response(request, {'subcat_id': s.pk})

def get_sub_category(request, subcat_id):
    if request.method != 'GET':
        return _error_response(request, "must make GET request")

    try:
        s = models.Subcategory.objects.get(pk=subcat_id)
    except models.Category.DoesNotExist:
        return _error_response(request, "category not found")

    return _success_response(request, {'title': s.title, 'category': s.category })

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
