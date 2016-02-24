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
	for curr_cat in deser: #curr_cat is the name of the category
		cells_dict[curr_cat] = {}
		print(curr_cat)
		cells_dict[curr_cat]["id"] = deser[curr_cat]['catID']
		cells_dict[curr_cat]["subcategories"] = deser[curr_cat]['subcategories']
		# for subcat in deser[cat]:
		# 	# cells_dict[cat].append(subcat)
		# 	cells_dict[cat][subcat] = subcat
	return render(request, 'home.html', {'cells_dict':cells_dict})
	#return JsonResponse(cells_dict, content_type='json', safe=False)
