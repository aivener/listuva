from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
import json
import requests

#get all info for home page

#get individual item info (if click it) -- price, comments, etc. - build it together, serialize into JSON, pass to top layer to turn into something to look at

def makeTable(request): #returns json: key=category, value=subcategory
	#get json of all categories and subcategories
	all_cats = requests.get('http://modelsul:8000/api/v1/category')
	all_subcats = requests.get('http://modelsul:8000/api/v1/subcategory')
	new_info = {} #set up dictionary to return
	deser_cats = json.loads(all_cats.text) #deserialize
	deser_subcats = json.loads(all_subcats.text)
	for cat in deser_cats:
		curr_cat_name = str(cat['fields']['title'])
		curr_cat_id = cat['pk']
		new_info[curr_cat_name] = {}
		new_info[curr_cat_name]["catID"] = curr_cat_id
		temp_value_arr = {}
		for subcat in deser_subcats:
			if(subcat['fields']['category'] == curr_cat_id):
				temp_value_arr[subcat['fields']['title']] = subcat['pk']
		new_info[curr_cat_name]["subcategories"] = temp_value_arr
	return JsonResponse(new_info, content_type='application/json')

def getPostsByCategory(request, catID): #returns json of posts in given category
	all_posts = requests.get('http://modelsul:8000/api/v1/post')
	all_cats = requests.get('http://modelsul:8000/api/v1/category')
	sorted_posts = {}
	deser_posts = json.loads(all_posts.text)
	deser_cats = json.loads(all_cats.text)
	for curr_cat in deser_cats:
		curr_cat_id = curr_cat['pk']
		if(int(curr_cat_id) == int(catID)):
			for post in deser_posts:
				if(int(post['fields']['category']) == int(catID)):
					fields = post['fields']
					sorted_posts[post['pk']] = {}
					sorted_posts[post['pk']]['fields'] = fields
	return JsonResponse(sorted_posts, content_type='application/json')

def getPostsBySubcategory(request, subcatID): #returns json of posts in given subcategory
	all_posts = requests.get('http://modelsul:8000/api/v1/post')
	all_subcats = requests.get('http://modelsul:8000/api/v1/subcategory')
	sorted_posts = {}
	deser_posts = json.loads(all_posts.text)
	deser_subcats = json.loads(all_subcats.text)
	for curr_subcat in deser_subcats:
		curr_subcat_id = curr_subcat['pk']
		if(int(curr_subcat_id) == int(subcatID)):
			for post in deser_posts:
				if(int(post['fields']['subcategory']) == int(subcatID)):
					fields = post['fields']
					sorted_posts[post['pk']] = {}
					sorted_posts[post['pk']]['fields'] = fields
	return JsonResponse(sorted_posts, content_type='application/json')

def getCatName(request, catID): #returns json key="catname", value=the name
	all_cats = requests.get('http://modelsul:8000/api/v1/category')
	new_info = {} #set up dictionary to return
	deser_cats = json.loads(all_cats.text) #deserialize
	for cat in deser_cats:
		curr_cat_id = int(cat['pk'])
		if(curr_cat_id == int(catID)):
			curr_cat_name = str(cat['fields']['title'])
			new_info["catName"] = curr_cat_name
	return JsonResponse(new_info, content_type='application/json')

def getSubcatName(request, subcatID):
	all_subcats = requests.get('http://modelsul:8000/api/v1/subcategory')
	new_info = {} #set up dictionary to return
	deser_subcats = json.loads(all_subcats.text) #deserialize
	for subcat in deser_subcats:
		curr_subcat_id = int(subcat['pk'])
		if(curr_subcat_id == int(subcatID)):
			curr_subcat_name = str(subcat['fields']['title'])
			new_info["subcatName"] = curr_subcat_name
	return JsonResponse(new_info, content_type='application/json')

def getCatNameFromSubcat(request, subcatID): #returns json key="cateogryName", value= the name
	all_cats = requests.get('http://modelsul:8000/api/v1/category')
	all_subcats = requests.get('http://modelsul:8000/api/v1/subcategory')
	new_info = {}
	deser_cats = json.loads(all_cats.text)
	deser_subcats = json.loads(all_subcats.text)
	for subcat in deser_subcats:
		curr_subcat_id = int(subcat['pk'])
		if(curr_subcat_id == int(subcatID)):
			catID = str(subcat['fields']['category'])
			for cat in deser_cats:
				curr_cat_id = int(cat['pk'])
				if(curr_cat_id == int(catID)):
					new_info["categoryName"] = str(cat['fields']['title'])
					return JsonResponse(new_info, content_type='application/json')
	return JsonResponse(new_info, content_type='application/json')


def login_exp_api(request): #takes in data from frontul login method to authenticate
	input_username = request.POST.get('username', 'default')
	input_password = request.POST.get('password', 'default')
	#get all students
	student_with_username = requests.get('http://modelsul:8000/api/v1/student/' + input_username)
	deser_student = json.loads(student_with_username.text) #TODO: add this url
	#check if that returned a student
	if student_with_username:
		#get hashed password of that username
		#check if equal to password passed into the method
		for curr_student in deser_student:
			real_pword = curr_student['fields']['password']
			if str.strip(real_pword) == str.strip(input_password):
				#successful match
				#new_auth = requests.post('http://modelsul:8000/api/v1/authenticator/' + str(curr_student['pk']))
				new_auth = requests.post('http://modelsul:8000/api/v1/authenticator/', data={"pk": curr_student['pk']})
				#return HttpResponse(new_auth)
				return JsonResponse(new_auth.json(), content_type="application/json", safe=False)
			else:
				# return JsonResponse({"log":"We hit an error2"}, content_type="application/json")
				return JsonResponse({}, content_type="application/json")
		# return JsonResponse({"log":"We hit an error1", "student": deser_student, "studentname": input_username} , content_type="application/json")
		return JsonResponse({} , content_type="application/json")
	else:
		# return JsonResponse({"log":"We hit an error"}, content_type="application/json")
		return JsonResponse({}, content_type="application/json")
