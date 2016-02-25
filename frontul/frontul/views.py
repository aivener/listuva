from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
import json
import requests
from django.shortcuts import render

def displayCells(request):
	cats_subcats = requests.get('http://expul:8000/api/v1/maketable')
	deser = json.loads(cats_subcats.text)
	return render(request, 'home.html', {'cells_dict':deser})
	#return JsonResponse(cells_dict, content_type='json', safe=False)

def displayPosts(request,catID):
	c = requests.get('http://expul:8000/api/v1/postbycat/' + catID)
	deser = json.loads(c.text)
	x = requests.get('http://expul:8000/api/v1/getcatname/' + catID)
	deser1 = json.loads(x.text)
	return render(request, 'posts.html', {'cells_dict':deser, 'catName': deser1})
