from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
import json
import requests

#get all info for home page

#get individual item info (if click it) -- price, comments, etc. - build it together, serialize into JSON, pass to top layer to turn into something to look at

def makeTable(request):
	#get json of all categories
	all_cats = requests.get('http://modelsul:8000/api/v1/category')
	all_subcats = requests.get('http://modelsul:8000/api/v1/subcategory')
	new_info = {}
	deser_cats = json.loads(all_cats.text)
	deser_subcats = json.loads(all_subcats.text)
	for cat in deser_cats:	
		curr_cat_name = str(cat['fields']['title'])
		curr_cat_id = cat['pk']
		new_info[curr_cat_name] = []
		for subcat in deser_subcats:
			if(subcat['fields']['category'] == curr_cat_id):
				new_info[curr_cat_name].append(subcat['fields']['title'])
	ser = json.dumps(new_info)
	return HttpResponse(ser, content_type='application/json')
	

	#get list of all posts
		#python request to models/api/v1/posts which returns json of all the posts
	#take that json, and get json of other stuff needed on home page
	#new json object with all the info 
	#return that json object via a url in this project