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


def displayCells(request):
	cats_subcats = requests.get('http://expul:8000/api/v1/maketable')
	deser = json.loads(cats_subcats.text)
	return render(request, 'home.html', {'cells_dict':deser})
	#return JsonResponse(cells_dict, content_type='json', safe=False)

def displayCatPosts(request,catID):
	c = requests.get('http://expul:8000/api/v1/postbycat/' + catID)
	deser = json.loads(c.text)
	x = requests.get('http://expul:8000/api/v1/getcatname/' + catID)
	deser1 = json.loads(x.text)
	return render(request, 'catposts.html', {'cells_dict':deser, 'catName': deser1})

def displaySubCatPosts(request,subCatID):
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
		next = request.GET.get('login') or reverse('displayCells') #??
		return render(request, 'login.html', {'form': l_form})
	
	f = LoginForm(request.POST)
	if not f.is_valid():
		# bogus form post, send them back to login page and show them an error
		return render('login.html', "")
	username = f.cleaned_data['username']
	password = f.cleaned_data['password']
	#next = f.cleaned_data.get('next') or reverse('home')
	next = reverse('displayCells') #reverse takes name of the view and returns the URL of the view
	resp = requests.post('http://expul:8000/api/v1/login_exp_api/', data={"username": username, "password": password})
	if not resp:
		# couldn't log them in, send them back to login page with error
		return render(request, 'login.html')
	# logged them in. set their login cookie and redirect to back to wherever they came from
	# authenticator = resp['authenticator']
	response = HttpResponseRedirect(next)
	# response.set_cookie("auth", authenticator)
	return response


# def create_post(request):
# 	auth = request.COOKIES.get('auth')
# 	if not auth:
# 		# handle user not logged in while trying to create a post
# 		return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_listing")
# 	if request.method == 'GET':
# 		return render("create_post.html", ...)
# 	f = create_listing_form(request.POST)
#     ...
# 	resp = create_listing_exp_api(auth, ...)
# 	if resp and not resp['ok']:
# 		if resp['error'] == exp_srvc_errors.E_UNKNOWN_AUTH:
# 			# exp service reports invalid authenticator -- treat like user not logged in
# 			return HttpResponseRedirect(reverse("login") + "?next=" + reverse("create_post")
# 	...
# 	return render("create_post_success.html", ...)