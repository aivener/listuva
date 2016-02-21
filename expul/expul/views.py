from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from .models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt 

#get all info for home page

#get individual item info (if click it) -- price, comments, etc. - build it together, serialize into JSON, pass to top layer to turn into something to look at

def makeTable():
	#get json of all categories
	result= requests.get('modelsul/api/v1/category')
	# status_code = result.status_code
	return HttpResponse(result, content_type='json')

	#get list of all posts
		#python request to models/api/v1/posts which returns json of all the posts
	#take that json, and get json of other stuff needed on home page
	#new json object with all the info 
	#return that json object via a url in this project