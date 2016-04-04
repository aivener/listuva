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
genders = (('1', 'Male'), ('2', 'Female'))

class LoginForm(forms.Form):
	email = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)

class SignUpForm(forms.Form):
	email = forms.CharField(required=False)
	password = forms.CharField(required=True, widget=forms.PasswordInput)
	name = forms.CharField(required=True)
	year = forms.IntegerField(required=True)
	gender = forms.CharField(required=True, widget=forms.Select(choices=genders))

class CreatePostForm(forms.Form):
	title = forms.CharField(required=True)
	category = forms.CharField(widget=forms.Select(choices=choices))
	subcategory = forms.CharField(required=True)
	summary = forms.CharField(required=True)
	price = forms.DecimalField(max_digits = 10, decimal_places = 2)

class SearchForm(forms.Form):
	searchText = forms.CharField(required=True, label='Query', max_length=50)