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
	cells_dict = {}
	for cat in deser:
		cells_dict[cat] = []
		for subcat in deser[cat]:
			cells_dict[cat].append(subcat)
	return render(request, 'home.html', {'cells_dict':cells_dict})
	#return JsonResponse(cells_dict, content_type='json', safe=False)

# def linkToPosts(request):
# 	cats_subcats = requests.get('http://expul:8000/api/v1/maketable')
# 	deser = json.loads(cats_subcats.text)
# 	cells_dict = {}
# 	for cat in deser:
# 		cells_dict[cat] = []
# 		for subcat in deser[cat]:
# 			cells_dict[cat].append(subcat)
# 	return render(request, 'home.html', {'cells_dict':cells_dict})
# 	#return JsonResponse(cells_dict, content_type='json', safe=False)