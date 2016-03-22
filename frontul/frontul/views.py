from django.http import HttpResponse

from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
import json
import requests
#import exp_srvc_errors  # where I put some error codes the exp srvc can return
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from django.core.urlresolvers import reverse
from .forms import *
from django.contrib.auth import hashers



def displayCells(request):
	auth = request.COOKIES.get('auth')
	if not auth:
		# handle user not logged in while trying to create a post
		return HttpResponseRedirect(reverse("login"))
	cats_subcats = requests.get('http://expul:8000/api/v1/maketable')
	deser = json.loads(cats_subcats.text)
	return render(request, 'home.html', {'cells_dict':deser})
	#return JsonResponse(cells_dict, content_type='json', safe=False)

def displayCatPosts(request,catID):
	auth = request.COOKIES.get('auth')
	if not auth:
		# handle user not logged in while trying to create a post
		return HttpResponseRedirect(reverse("login"))
	c = requests.get('http://expul:8000/api/v1/postbycat/' + catID)
	deser = json.loads(c.text)
	x = requests.get('http://expul:8000/api/v1/getcatname/' + catID)
	deser1 = json.loads(x.text)
	return render(request, 'catposts.html', {'cells_dict':deser, 'catName': deser1})

def displaySubCatPosts(request,subCatID):
	auth = request.COOKIES.get('auth')
	if not auth:
		# handle user not logged in while trying to create a post
		return HttpResponseRedirect(reverse("login"))
	c = requests.get('http://expul:8000/api/v1/postbysubcat/' + subCatID)
	deser = json.loads(c.text)
	x = requests.get('http://expul:8000/api/v1/getsubcatname/' + subCatID)
	deser1 = json.loads(x.text)
	y = requests.get('http://expul:8000/api/v1/catname/' + subCatID)
	deser2 = json.loads(y.text)
	return render(request, 'subcatposts.html', {'cells_dict':deser, 'subCatName': deser1, 'catName': deser2})

#called when user submits login form
def login(request):
	if request.method == 'GET':
		l_form = LoginForm()
		next = request.GET.get('login') or reverse('displayCells')
		return render(request, 'login.html', {'form': l_form})
	f = LoginForm(request.POST)
	if not f.is_valid():
		# bogus form post, send them back to login page and show them an error
		return render('login.html', "")
	username = f.cleaned_data['username']
	password = hashers.make_password(f.cleaned_data['password'], salt="bar") #hashes password that was typed into form - this works
	#return HttpResponse(password)
	
	#next = f.cleaned_data.get('next') or reverse('home')
	next = reverse('displayCells') #reverse takes name of the view and returns the URL of the view
	
	#send typed username and hashed password to exp level
	resp = requests.post('http://expul:8000/api/v1/login_exp_api/', data={"username": username, "password": password}).json()
	#return JsonResponse(resp.json(), safe=False)
	if not resp or not resp[0]['pk']: #no student with that username/password, send back to login page with error
		return HttpResponseRedirect(reverse('login'))

	# logged them in. set their login cookie and redirect to back to wherever they came from
	authenticator = resp[0]['pk']
	response = HttpResponseRedirect(next)
	response.set_cookie("auth", authenticator)
	return response

def signup(request):
	if request.method == 'GET':
		s_form = SignUpForm()
		next = request.GET.get('signup') or reverse('displayCells')
		return render(request, 'signup.html', {'form': s_form})
	f = SignUpForm(request.POST)
	if not f.is_valid():
		# bogus form post, send them back to login page and show them an error
		return HttpResponseRedirect('/blah/')
	username = f.cleaned_data['username']
	password = f.cleaned_data['password']
	name = f.cleaned_data['name']
	year = f.cleaned_data['year']
	gender = f.cleaned_data['gender']
	next = reverse('login')
	resp = requests.post('http://expul:8000/api/v1/signup_exp_api/', data={"username":username,"password":password,"name":name,"year":year, "gender":gender}).json()
	response = HttpResponseRedirect(next)
	return response


def create_post(request):
	auth = request.COOKIES.get('auth')
	if not auth:
		# handle user not logged in while trying to create a post
		return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_post"))
	if request.method == 'GET':
		all_cat = requests.get('http://expul:8000/api/v1/getallcatname/')
		post_form = CreatePostForm(initial={'cat_choices': json})
		return render(request, "create_post.html", {'form': post_form})
	f = CreatePostForm(request.POST)
	if not f.is_valid():
		# bogus form post, send them back to login page and show them an error
		return HttpResponseRedirect('/blah/')
	title = f.cleaned_data['title']
	category = f.cleaned_data['category']
	subcategory = f.cleaned_data['subcategory']
	summary = f.cleaned_data['summary']
	price = f.cleaned_data['price']
	next = reverse('displayCells')
	resp = requests.post('http://expul:8000/api/v1/create_listing_exp_api/', data={"title":title, "category":category, "subcategory":subcategory, "summary":summary, "price":price, "auth":auth}).json()
	response = HttpResponseRedirect(next)
	return response

#     ...
	#resp = create_listing_exp_api(auth, ...)
# 	if resp and not resp['ok']:
# 		if resp['error'] == exp_srvc_errors.E_UNKNOWN_AUTH:
# 			# exp service reports invalid authenticator -- treat like user not logged in
# 			return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_post")
# 	...
# 	return render("create_post_success.html", ...)


#delete auth cookie and delete auth from database
def logoutUser(request):
	response = HttpResponseRedirect(reverse('displayCells'))
	response.delete_cookie("auth")
	return response











