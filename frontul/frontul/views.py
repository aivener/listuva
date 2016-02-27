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
