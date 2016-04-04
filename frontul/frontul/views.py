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
from django.contrib import messages
from django.shortcuts import render_to_response



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

def displaySinglePost(request,postID):
	# auth = request.COOKIES.get('auth')
	# if not auth:
	# 	# handle user not logged in while trying to see posts
	# 	return HttpResponseRedirect(reverse("login"))
	c = requests.get('http://expul:8000/api/v1/getPost/' + postID)
	ps = c.json()

	scatNum = ps['subcategory']
	subcat = requests.get('http://expul:8000/api/v1/getsubcatname/' + str(scatNum))
	r = subcat.json()

	catNum = ps['category']
	cat = requests.get('http://expul:8000/api/v1/getcatname/' + str(catNum))
	c = cat.json()


	return render(request, 'post.html', {'post':ps, 'subcat': r, 'cat': c})

#called when user submits login form
def login(request):
	auth = request.COOKIES.get('auth')
	if auth: #already logged in, redirect to home page
		return HttpResponseRedirect(reverse("displayCells"))

	if request.method == 'GET':
		l_form = LoginForm()
		next = request.GET.get('login') or reverse('displayCells')
		return render(request, 'login.html', {'form': l_form})
	f = LoginForm(request.POST)
	if not f.is_valid():
		# bogus form post, send them back to login page and show them an error
		messages.error(request, 'You must fill out all fields')
		return HttpResponseRedirect('/login/')
	email = f.cleaned_data['email']
	password = f.cleaned_data['password']
	#next = f.cleaned_data.get('next') or reverse('home')
	next = reverse('displayCells') #reverse takes name of the view and returns the URL of the view

	#send typed email and password to exp level
	resp = requests.post('http://expul:8000/api/v1/login_exp_api/', data={"email": email, "password": password}).json()
	#return HttpResponse(resp)
	#return JsonResponse(resp.json(), safe=False)
	if not resp or not resp[0]['pk']: #no student with that username/password, send back to login page with error
		messages.error(request, 'Invalid username and/or password.')
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
		messages.error(request, 'You must fill out all fields!')
		return HttpResponseRedirect('/signup/')
	email = f.cleaned_data['email']
	password = f.cleaned_data['password']
	name = f.cleaned_data['name']
	year = f.cleaned_data['year']
	gender = f.cleaned_data['gender']
	next = reverse('login')
	resp = requests.post('http://expul:8000/api/v1/signup_exp_api/', data={"email":email,"password":password,"name":name,"year":year, "gender":gender}).json()
	response = HttpResponseRedirect(next)
	return response

def search(request):
	if request.method == 'GET':
		s_form = SearchForm()
		next = request.GET.get('search') or reverse('displayCells')
		return render(request, 'search.html', {'form': s_form})
	f = SearchForm(request.POST)
	if not f.is_valid():
		messages.error(request, 'You must fill out all fields!')
		return HttpResponseRedirect('/search/')
	searchText = f.cleaned_data['searchText']
	next = reverse('search')
	resp = requests.post('http://expul:8000/api/v1/search/', data={"searchText":searchText})
	resp_data = json.loads(resp.text)
	# response = HttpResponseRedirect(next)
	return render_to_response('search.html', {"posts": resp_data})

def create_post(request):
	auth = request.COOKIES.get('auth')
	if not auth:
		# handle user not logged in while trying to create a post
		return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_post"))
	des_catergories = requests.get('http://expul:8000/api/v1/getallcatname/')
	des_subcatergories = requests.get('http://expul:8000/api/v1/getallsubcatname/')
	catergories = json.loads(des_catergories.text)
	subcategories = json.loads(des_subcatergories.text)
	cat_names = []
	cat_nums = []
	for val in catergories:
		cat_nums.append(val)
		cat_names.append(catergories[val])
	cat_choices = zip(cat_nums, cat_names)

	subcat_cats = []
	subcat_fields = []
	for val1 in subcategories:
		pks = []
		names = []
		for val2 in subcategories[val1]:
			pks.append(val2)
			names.append(subcategories[val1][val2])
		prim_choices = zip(pks, names)
		subcat_fields.append(prim_choices)
		subcat_cats.append(val1)
	subcat_choices = zip(subcat_cats, subcat_fields)

	if request.method == 'GET':
		all_cat = requests.get('http://expul:8000/api/v1/getallcatname/')

		post_form = CreatePostForm()
		return render(request, "create_post.html", {'form': post_form, 'choices':subcat_choices, 'text': "hello", 'cat_choices':cat_choices})
	f = CreatePostForm(request.POST)

	if not f.is_valid():
		# bogus form post, send them back to login page and show them an error
		messages.error(request, 'Error: Please fill out all fields appropriately!')
		return HttpResponseRedirect('/create_post/')
	if f.cleaned_data['category'] == "null" or f.cleaned_data['subcategory'] == "null":
		messages.error(request, 'You must fill out all fields!')
		return HttpResponseRedirect('/create_post/')
	#return HttpResponse(f.cleaned_data['category'])
	title = f.cleaned_data['title']
	category = f.cleaned_data['category']
	subcategory = f.cleaned_data['subcategory']
	summary = f.cleaned_data['summary']
	price = f.cleaned_data['price']
	next = reverse('displayCells')

	resp = requests.post('http://expul:8000/api/v1/create_listing_exp_api/', data={"title":title, "category":category, "subcategory":subcategory, "summary":summary, "price":price, "auth":auth})
	response = HttpResponseRedirect(next)
	return response


#delete auth cookie and delete auth from database
def logoutUser(request):
	response = HttpResponseRedirect(reverse('displayCells'))
	response.delete_cookie("auth")
	return response
