from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
import json
import requests

#get all info for home page

#get individual item info (if click it) -- price, comments, etc. - build it together, serialize into JSON, pass to top layer to turn into something to look at

def makeTable(request):
	#get json of all categories and subcategories
	all_cats = requests.get('http://modelsul:8000/api/v1/category')
	all_subcats = requests.get('http://modelsul:8000/api/v1/subcategory')
	new_info = {} #set up dictionary to return
	deser_cats = json.loads(all_cats.text) #deserialize
	deser_subcats = json.loads(all_subcats.text)
	for cat in deser_cats:	
		curr_cat_name = str(cat['fields']['title'])
		curr_cat_id = cat['pk']
		new_info[curr_cat_name] = []
		for subcat in deser_subcats:
			if(subcat['fields']['category'] == curr_cat_id):
				new_info[curr_cat_name].append(subcat['fields']['title'])
	return JsonResponse(new_info, content_type='application/json')
