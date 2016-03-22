from django import forms
import requests
from django.core import serializers
import json

catergories = requests.get('http://expul:8000/api/v1/getallcatname/')
data = json.loads(catergories.text)
names = []
nums = []
for val in data:
	nums.append(val)
	names.append(data[val])
choices = zip(nums, names)

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True)

class SignUpForm(forms.Form):
	username = forms.CharField(required=False)
	password = forms.CharField(required=True)
	name = forms.CharField(required=True)
	year = forms.IntegerField(required=True)
	gender = forms.BooleanField(required=True)

class CreatePostForm(forms.Form):
	title = forms.CharField(required=True)
	category = forms.CharField(widget=forms.Select(choices=choices))
	subcategory = forms.CharField(required=True)
	summary = forms.CharField(required=True)
	price = forms.DecimalField(max_digits = 10, decimal_places = 2)